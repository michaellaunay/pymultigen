from pathlib import Path
import builtins
from unittest import mock

import jinja2
import pytest

from multigen.generator import Task
from multigen.jinja import JinjaTask, JinjaGenerator


def test_current_directory(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    Task.ensure_folder('result.txt')
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('failure', ['render', 'formatter'])
@pytest.mark.parametrize('existing', [False, True])
def test_failure_preserves_destination(tmp_path, failure, existing):
    target = tmp_path / 'result.txt'
    if existing:
        target.write_text('previous', encoding='utf-8')
    task = JinjaTask()
    task.template_name = 'test'
    task.environment = jinja2.Environment(loader=jinja2.DictLoader(
        {'test': '{{ missing.value }}' if failure == 'render' else 'text'}))
    if failure == 'formatter':
        def fail(text):
            raise ValueError('formatter failed')
        task.formatter = fail
    with pytest.raises((jinja2.UndefinedError, ValueError)):
        task.generate_file(None, target)
    assert target.read_text(encoding='utf-8') == 'previous' if existing else not target.exists()


def test_utf8_explicit(tmp_path):
    task = JinjaTask()
    task.template_name = 'test'
    task.environment = jinja2.Environment(loader=jinja2.DictLoader({'test': 'été 日本語'}))
    real_open = builtins.open
    def checked_open(*args, **kwargs):
        assert kwargs.get('encoding') == 'utf-8'
        return real_open(*args, **kwargs)
    with mock.patch('multigen.jinja.open', side_effect=checked_open, create=True):
        task.generate_file(None, tmp_path / 'unicode.txt')
    assert (tmp_path / 'unicode.txt').read_bytes() == 'été 日本語'.encode('utf-8')


def test_multifile_determinism_and_paths(tmp_path):
    class Files(JinjaTask):
        template_name = 'test'
        def filtered_elements(self, model):
            return iter(model)
        def relative_path_for_element(self, element):
            return element
    task = Files(formatter=lambda text: text.upper())
    class FilesGenerator(JinjaGenerator):
        def __init__(self, **kwargs):
            self.tasks = [task]
            super().__init__(**kwargs)
    generator = FilesGenerator(environment=jinja2.Environment(
        loader=jinja2.DictLoader({'test': '{{ element }}'})))
    root = tmp_path / 'output'
    paths = ['nested/été.txt', 'other.txt']
    generator.generate(paths, root)
    first = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    generator.generate(paths, root)
    assert first == {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    assert first[Path('nested/été.txt')] == 'NESTED/ÉTÉ.TXT'.encode('utf-8')


@pytest.mark.parametrize('absolute', [False, True])
def test_legacy_outside_paths(tmp_path, absolute):
    # Only controlled temporary locations: historical API does not confine output.
    root = tmp_path / 'output'
    root.mkdir()
    target = tmp_path / 'outside.txt'
    task = JinjaTask()
    task.relative_path_for_element = lambda element: target if absolute else '../outside.txt'
    task.template_name = 'test'
    task.environment = jinja2.Environment(loader=jinja2.DictLoader({'test': 'ok'}))
    task.run(None, root)
    assert target.read_text() == 'ok'


def test_stream_closed_after_write_failure(tmp_path):
    task = JinjaTask()
    task.template_name = 'test'
    task.environment = jinja2.Environment(loader=jinja2.DictLoader({'test': 'text'}))
    streams = []
    class BrokenWriter:
        def __init__(self, *args, **kwargs):
            self.stream = builtins.open(*args, **kwargs)
            streams.append(self.stream)
        def __enter__(self):
            return self
        def write(self, text):
            self.stream.write(text[:1])
            raise OSError('controlled write failure')
        def __exit__(self, *exc):
            self.stream.close()
    with mock.patch('multigen.jinja.open', BrokenWriter, create=True):
        with pytest.raises(OSError, match='controlled write failure'):
            task.generate_file(None, tmp_path / 'partial.txt')
    assert streams[0].closed
    assert (tmp_path / 'partial.txt').read_text() == 't'
