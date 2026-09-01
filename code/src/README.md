# `code/src/`

Python source-layout 根目录，正式包位于 `mol_sql/`。采用该布局可避免从仓库根目录误导入未安装的同名模块。

## 使用

开发时设置：

```bash
export PYTHONPATH=code/src
python -m mol_sql.cli --help
```

也可在独立环境中执行 `python -m pip install -e code`。本目录只放包源码，不保存配置、数据或运行产物。
