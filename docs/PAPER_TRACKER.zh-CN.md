# AG-ReID 自动论文追踪器

这个追踪器把“发现论文”和“正式收录”分成两个阶段：

1. `Discover AG-ReID Papers` 每周查询 arXiv、OpenAlex、Crossref 和 DBLP。
2. 本地规则执行相关性评分、跨数据源合并以及与 README 的去重。
3. 尚未收录的结果进入一个滚动 GitHub Issue，等待人工审核。
4. 维护者确认后运行 `Accept paper candidate`，自动创建修改中英文 README 的 PR。
5. PR 合并后，原有 `Update Publication Trend Chart` workflow 重新生成趋势图。

追踪器不会把外部检索结果直接写进正式清单。

## 启用

Fork 仓库以后：

1. 打开仓库的 **Actions** 页面，启用 workflows。
2. 进入 **Settings → Actions → General → Workflow permissions**。
3. 允许 GitHub Actions 创建 Pull Request。组织策略更严格时，需要组织管理员开放对应权限。
4. 可选：在 **Settings → Secrets and variables → Actions** 中添加：
   - Secret `OPENALEX_API_KEY`：OpenAlex 免费 API key；不配置也可进行小规模匿名查询。
   - Variable `PAPER_TRACKER_EMAIL`：Crossref polite pool 使用的联系邮箱。
5. 在 Actions 页面手动运行一次 **Discover AG-ReID Papers** 验证配置。

定时任务默认每周一 UTC 02:17 运行。选择非整点是为了降低 GitHub Actions 高峰期延迟。

## 审核候选论文

自动创建的 Issue 会给出标题、规范链接、作者、日期、venue、稳定标识符、数据来源、相关性分数、命中原因和建议分类。

请人工确认：

- 论文是否真正研究空中—地面目标重识别；
- arXiv 和正式发表版本是否为同一篇论文；
- venue 是否已经正式确认，论文是否改过标题；
- 代码、数据集和项目链接是否为作者官方资源；
- 应放入图像、视频、车辆、挑战还是相关探索分类。

## 将确认的候选变成 PR

打开 **Actions → Accept paper candidate → Run workflow**，填写目标分类、venue 与年份、方法简称、准确标题和论文链接，以及可选的代码、数据集和项目链接。

任务会在新分支中同时修改 `README.md` 和 `README.zh-CN.md`，然后创建 PR。合并前仍应检查表格顺序和所有元数据。

如果 GitHub 报错不允许创建 PR，请重新检查仓库的 Actions 权限；这项权限在部分 Fork 和组织仓库中默认关闭。

## 忽略误报

编辑 `config/paper-tracker.json`：

```json
{
  "ignored_identifiers": [
    "arxiv:2601.12345",
    "doi:10.1234/example"
  ],
  "ignored_titles": [
    "An unrelated UAV Re-Identification paper"
  ]
}
```

优先使用 arXiv ID 或 DOI；标题只用于没有稳定标识符的记录。

## 调整召回率

配置文件中的 `lookback_days` 控制回查天数，`max_results_per_query` 控制每次查询数量，`max_candidates` 控制 Issue 长度，`minimum_score` 控制最低相关性，`sources` 和 `queries` 控制数据源与关键词。

本地运行：

```bash
python3 scripts/paper_tracker.py
python3 -m unittest discover -s tests -v
```

结果保存在 `.paper-tracker/report.md` 和 `.paper-tracker/candidates.json`。该目录不会提交，Actions 会将其作为临时 artifact 保存 30 天。

## 已知边界

- 每周检索不等于绝对实时，各索引可能延迟收录。
- CVF Open Access 没有加入自动网页抓取，因为页面结构容易变化；会议官网和作者主页仍应人工核验。
- 自动分类只是建议，尤其是 challenge、dataset、text-to-person 和 gait 类论文。
- 标题模糊匹配可以发现改名论文，但极端改名仍可能重复。
- 任一数据源暂时失败时，其余数据源仍会继续运行，报告会列出失败信息。

## 数据源

- [arXiv API](https://info.arxiv.org/help/api/user-manual.html)
- [OpenAlex API](https://help.openalex.org/api/)
- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [DBLP Search API](https://dblp.org/search/publ/api)
