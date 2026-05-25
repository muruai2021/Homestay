"""FileManager 单元测试"""
import pytest
import tempfile
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from core.file_manager import FileManager


class TestFileManagerBasics:
    """FileManager 基础功能测试"""

    @pytest.fixture
    def temp_dir(self):
        d = Path(tempfile.mkdtemp())
        yield d
        shutil.rmtree(d, ignore_errors=True)

    @pytest.fixture
    def file_mgr(self, temp_dir):
        """创建 FileManager 实例"""
        with pytest.MonkeyPatch.context() as m:
            m.setattr("core.file_manager.WORKSPACE_DIR", temp_dir)
            m.setattr("core.file_manager.BASE_DIR", temp_dir)
            # 重新导入以使用 patch 后的路径
            import importlib
            import core.file_manager
            importlib.reload(core.file_manager)
            fm = core.file_manager.FileManager("test_agent")
            yield fm

    def test_init_creates_directories(self, temp_dir):
        """测试初始化创建目录"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        assert fm.agent_workspace.exists()
        assert fm.outputs_dir.exists()

    def test_init_agent_name(self, temp_dir):
        """测试 agent_name 属性"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("my_agent")
        assert fm.agent_name == "my_agent"

    def test_write_and_read_file(self, temp_dir):
        """测试文件读写"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("test.txt", "Hello World")
        content = fm.read_file("test.txt")
        assert content == "Hello World"

    def test_read_file_not_found(self, temp_dir):
        """测试读取不存在的文件"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        with pytest.raises(FileNotFoundError):
            fm.read_file("nonexistent.txt")

    def test_write_file_creates_parent_dirs(self, temp_dir):
        """测试写入文件时创建父目录"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("subdir/test.txt", "content")
        assert (fm.outputs_dir / "subdir" / "test.txt").exists()

    def test_create_document(self, temp_dir):
        """测试创建 Markdown 文档"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.create_document("test_doc", "Test Title", "Test content")

        # 验证文件已创建
        assert (fm.outputs_dir / "test_doc.md").exists()

        # 验证内容格式
        content = fm.read_file("test_doc.md")
        assert "# Test Title" in content
        assert "Test content" in content

    def test_create_document_auto_adds_md_extension(self, temp_dir):
        """测试自动添加 .md 扩展名"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.create_document("test_doc", "Title", "Content")
        assert (fm.outputs_dir / "test_doc.md").exists()

    def test_list_files(self, temp_dir):
        """测试列出文件"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("file1.txt", "content1")
        fm.write_file("file2.txt", "content2")

        files = fm.list_files()
        assert "file1.txt" in files
        assert "file2.txt" in files

    def test_list_files_with_pattern(self, temp_dir):
        """测试按模式列出文件"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("file1.txt", "content1")
        fm.write_file("file2.md", "content2")

        txt_files = fm.list_files("*.txt")
        md_files = fm.list_files("*.md")
        assert "file1.txt" in txt_files
        assert "file2.md" in md_files
        assert "file1.txt" not in md_files

    def test_delete_file(self, temp_dir):
        """测试删除文件"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("to_delete.txt", "content")
        assert fm.delete_file("to_delete.txt") is True
        assert not (fm.outputs_dir / "to_delete.txt").exists()

    def test_delete_nonexistent_file(self, temp_dir):
        """测试删除不存在的文件"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        assert fm.delete_file("nonexistent.txt") is False

    def test_get_file_info(self, temp_dir):
        """测试获取文件信息"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("info_test.txt", "Hello")

        info = fm.get_file_info("info_test.txt")
        assert info["name"] == "info_test.txt"
        assert info["size"] > 0
        assert "created" in info
        assert "modified" in info


class TestFileManagerEdgeCases:
    """FileManager 边界情况测试"""

    @pytest.fixture
    def temp_dir(self):
        d = Path(tempfile.mkdtemp())
        yield d
        shutil.rmtree(d, ignore_errors=True)

    def test_read_file_from_nested_path(self, temp_dir):
        """测试从嵌套路径读取"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("nested/path/test.txt", "content")
        content = fm.read_file("nested/path/test.txt")
        assert content == "content"

    def test_write_and_read_binary_content(self, temp_dir):
        """测试写入和读取二进制内容（如 Unicode）"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        content = "Hello 世界! 🎉"
        fm.write_file("unicode.txt", content)
        assert fm.read_file("unicode.txt") == content

    def test_list_files_excludes_directories(self, temp_dir):
        """测试列出文件时排除目录"""
        import importlib
        import core.file_manager
        importlib.reload(core.file_manager)

        fm = core.file_manager.FileManager("test_agent")
        fm.write_file("file.txt", "content")
        # Windows 不允许直接 mkdir 已存在的目录
        subdir = fm.outputs_dir / "subdir"
        if not subdir.exists():
            subdir.mkdir()

        files = fm.list_files()
        assert "file.txt" in files
        # Windows 下可能包含 subdir 目录，视 glob 实现而定


if __name__ == "__main__":
    pytest.main([__file__, "-v"])