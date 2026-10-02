# 😎 Awesome Aerial-Ground Object Re-Identification

<p align="middle">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://github.com/YangQiWei3/Awesome-Aerial-Ground-Object-Re-Identification/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="Maintenance"></a>
  <a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License MIT"></a>
</p>

<p align="center">
  English | <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="leaderboards/ag_reid_leaderboards.pdf">🏆  Leaderboards</a>
</p>

A curated list of **Aerial-Ground Object Re-Identification (AG-ReID)** papers, datasets, codebases and challenges.  
AG-ReID aims to match Object across **aerial views** and **ground views**, facing major challenges such as extreme viewpoint discrepancy, scale/resolution variation, illumination changes and background clutter.

> 📩 Feel free to open an issue / PR to add papers, code or datasets.

## 📖 Table of Contents
- [😎 Awesome Aerial-Ground Object Re-Identification](#-awesome-aerial-ground-object-re-identification)
  - [📖 Table of Contents](#-table-of-contents)
  - [🌟 Spotlight: Our Contributions](#-spotlight-our-contributions)
  - [📊 Publication Trends](#-publication-trends)
  - [📝 Papers \& Methods](#-papers--methods)
    - [Image-based Person AG-ReID](#image-based-person-ag-reid)
    - [Image-based Vehicle AG-ReID](#image-based-vehicle-ag-reid)
    - [Video-based Person AG-ReID](#video-based-person-ag-reid)
    - [Challenges \& Workshops](#challenges--workshops)
  - [💾 Datasets](#-datasets)
    - [More Related Exploration](#more-related-exploration)
  - [🤖 Automatic Paper Tracking](#-automatic-paper-tracking)
  - [📈 Star History](#-star-history)
  - [🤝 Contributing](#-contributing)
  - [🤝 Acknowledgments](#-acknowledgments)
  - [📧 Contact](#-contact)
  - [📌 Citation](#-citation)

---

## 🌟 Spotlight: Our Contributions

Selected works from our research group on **cross-view alignment** and **robust representation learning**:

- **[ECCV 2026]** HiHR: Hierarchical Hyperbolic Representation for Aerial-Ground Person Re-Identification  [Paper](https://arxiv.org/abs/2607.09186) · [Code](https://github.com/YangQiWei3/HiHR)

- **[WACVW 2026]** SAS-VPReID: A Scale-Adaptive Framework with Shape Priors for Video-based Object Re-Identification at Extreme Far Distances  [Paper](https://arxiv.org/pdf/2601.05535) · [Code](https://github.com/YangQiWei3/SAS-VPReID)

- **[TIP 2026]** SD-ReID: View-aware Stable Diffusion for Aerial-Ground Object Re-Identification  [Paper](https://arxiv.org/abs/2504.09549)

- **[arXiv 2025]** LATex: Leveraging Attribute-based Text Knowledge for Aerial-Ground Object Re-Identification  [Paper](https://arxiv.org/abs/2503.23722)

> 📩 Feel free to open an issue if you have any questions about our paper.
---


## 📊 Publication Trends
Automatic statistics based on the papers listed in this repository.

![Publication Trend](assets/publication_trend.svg)

---

## 📝 Papers & Methods

### Image-based Person AG-ReID

| Conference / Journal | Method | Title | Resources | Framework |
| :------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **CVPR 2026** | UAD | WHU-MARS: A Multispectral Aerial-Ground Benchmark Towards  Any-Scenario Person Re-Identification | [Paper](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhao_WHU-MARS_A_Multispectral_Aerial-Ground_Benchmark_Towards_Any-Scenario_Person_Re-Identification_CVPR_2026_paper.pdf) | <img src="assets/frameworks/uad.png" width="320" alt="WHU-MARS: A Multispectral Aerial-Ground Benchmark Towards Any-Scenario Person Re-Identification — Figure 3"><br><sub>Original paper figure: [Figure 3](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhao_WHU-MARS_A_Multispectral_Aerial-Ground_Benchmark_Towards_Any-Scenario_Person_Re-Identification_CVPR_2026_paper.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **ECCV 2026** | MCVL | MCVL: Multi-Space Cross-View Learning for Aerial-Ground Person Re-Identification | [Paper](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/7411.pdf) | <img src="assets/frameworks/mcvl.png" width="320" alt="MCVL: Multi-Space Cross-View Learning for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/7411.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **ArXiv 2026** | VR3D | VR3D: View-Robust 3D Representation Learning for Aerial-Ground Person  Re-Identification | [Paper](https://arxiv.org/abs/2608.02598) | <img src="assets/frameworks/vr3d.png" width="320" alt="VR3D: View-Robust 3D Representation Learning for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2608.02598v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ECCV 2026** | HiHR | Hierarchical Hyperbolic Representation for Aerial-Ground Person Re-Identification | [Paper](https://arxiv.org/abs/2607.09186) · [Code](https://github.com/YangQiWei3/HiHR) | <img src="assets/frameworks/hihr.png" width="320" alt="Hierarchical Hyperbolic Representation for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2607.09186v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ArXiv 2026** | GeoReID | Rectifying Geometry-Induced Similarity Distortions for Real-World Aerial-Ground Person Re-Identification | [Paper](https://arxiv.org/abs/2601.21405) · [Code](https://github.com/kailashhambarde/GeoReID.git) | <img src="assets/frameworks/georeid.png" width="320" alt="Rectifying Geometry-Induced Similarity Distortions for Real-World Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2601.21405v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ECCV 2026** | 3D-LENS | 3D-LENS: A 3D Lifting-based Elevated Novel-view Synthesis method for Single-View  Aerial-Ground Re-Identification | [Paper](https://arxiv.org/abs/2604.26520) · [Code](https://github.com/TurtleSmoke/3D-LENS) | <img src="assets/frameworks/3d-lens.png" width="320" alt="3D-LENS: A 3D Lifting-based Elevated Novel-view Synthesis method for Single-View Aerial-Ground Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2604.26520v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **CVPR 2026** | ViSA | View-Aware Semantic Alignment for Aerial-Ground Person Re-Identification | [Paper](https://arxiv.org/abs/2605.18192) | <img src="assets/frameworks/visa.png" width="320" alt="View-Aware Semantic Alignment for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2605.18192v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **CVPR 2026** | CFAN | Cross-modal Fuzzy Alignment Network for Text-Aerial Person Retrieval and A Large-scale Benchmark | [Paper](https://arxiv.org/abs/2603.20721) | <img src="assets/frameworks/cfan.png" width="320" alt="Cross-modal Fuzzy Alignment Network for Text-Aerial Person Retrieval and A Large-scale Benchmark — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2603.20721v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **PRCV 2026** | GLPSG | Global-local prompts-driven semantic guidance for aerial-ground person re-identification | [Paper](https://link.springer.com/chapter/10.1007/978-981-95-5755-4_7) | <img src="assets/frameworks/glpsg.png" width="320" alt="Global-local prompts-driven semantic guidance for aerial-ground person re-identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://link.springer.com/content/pdf/10.1007/978-981-95-5755-4_7) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **AAAI 2026** | TAG-CLIP | Text-based Aerial-Ground Object Retrieval | [Paper](https://arxiv.org/pdf/2511.08369) · [Code](https://github.com/Flame-Chasers/TAG-PR) | <img src="assets/frameworks/tag-clip.png" width="320" alt="Text-based Aerial-Ground Object Retrieval — Figure 4"><br><sub>Original paper figure: [Figure 4](https://arxiv.org/pdf/2511.08369v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **AAAI 2026** | SVPR-ReID | Semantic-Driven Visual Progressive Refinement for Aerial-Ground Person ReID:  A Challenging Large-Scale Benchmark | [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/38339) | <img src="assets/frameworks/svpr-reid.png" width="320" alt="Semantic-Driven Visual Progressive Refinement for Aerial-Ground Person ReID: A Challenging Large-Scale Benchmark — Figure 2"><br><sub>Original paper figure: [Figure 2](https://ojs.aaai.org/index.php/AAAI/article/download/38339/42301) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **NeurIPS 2025** | GSAlign | Geometric and Semantic Alignment Network for Aerial-Ground Person Re-Identification | [Paper](https://openreview.net/attachment?id=bxELEjg3VE&name=pdf) · [Code](https://github.com/stone96123/GSAlign?tab=readme-ov-file) | <img src="assets/frameworks/gsalign.png" width="320" alt="Geometric and Semantic Alignment Network for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://proceedings.neurips.cc/paper_files/paper/2025/file/86c17de05579cde52025f9984e6e2ebb-Paper-Conference.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **ICCV 2025** | VIF | Bridging the Sky and Ground: Towards View-Invariant Feature Learning for Aerial-Ground Person Re-Identification | [Paper](https://openaccess.thecvf.com/content/ICCV2025/html/Khalid_Bridging_the_Sky_and_Ground_Towards_View-Invariant_Feature_Learning_for_ICCV_2025_paper.html) | <img src="assets/frameworks/vif.png" width="320" alt="Bridging the Sky and Ground: Towards View-Invariant Feature Learning for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://openaccess.thecvf.com/content/ICCV2025/papers/Khalid_Bridging_the_Sky_and_Ground_Towards_View-Invariant_Feature_Learning_for_ICCV_2025_paper.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **TIP 2026** | SD-ReID | View-aware Stable Diffusion for Aerial-Ground Person Re-Identification | [Paper](https://arxiv.org/abs/2504.09549) · [Code](https://github.com/924973292/SD-ReID) | <img src="assets/frameworks/sd-reid.png" width="320" alt="View-aware Stable Diffusion for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2504.09549v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ArXiv 2025** | LATex | Leveraging Attribute-based Text Knowledge for Aerial-Ground Person Re-Identification | [Paper](https://arxiv.org/abs/2503.23722) | <img src="assets/frameworks/latex.png" width="320" alt="Leveraging Attribute-based Text Knowledge for Aerial-Ground Person Re-Identification — Figure 3"><br><sub>Original paper figure: [Figure 3](https://arxiv.org/pdf/2503.23722v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ICME 2025** | DTST | Dynamic Token Selective Transformer for  Aerial-Ground Person Re-Identification | [Paper](https://yuhaiw.github.io/DTS-AGPReID/ICMEYuhai.pdf) · [Code](https://github.com/YuhaiW/reidselecttoken) | <img src="assets/frameworks/dtst.png" width="320" alt="Dynamic Token Selective Transformer for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://yuhaiw.github.io/DTS-AGPReID/ICMEYuhai.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **CVPR 2025** | SeCap | Self-Calibrating and Adaptive Prompts for Cross-view Person Re-Identification in Aerial-Ground Networks | [Paper](https://arxiv.org/abs/2503.06965) · [Code](https://github.com/wangshining681/SeCap-AGPReID) | <img src="assets/frameworks/secap.png" width="320" alt="Self-Calibrating and Adaptive Prompts for Cross-view Person Re-Identification in Aerial-Ground Networks — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2503.06965v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **TOMM 2025** | CVAF | A CLIP-Based View-Consistent Alignment Framework for Aerial-Ground Person Re-Identification | [Paper](https://dl.acm.org/doi/pdf/10.1145/3785482) | <img src="assets/frameworks/cvaf.png" width="320" alt="A CLIP-Based View-Consistent Alignment Framework for Aerial-Ground Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://dl.acm.org/doi/pdf/10.1145/3785482) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **ICIG 2025** | PDPA | Perspective Driven Prototype Alignment for Aerial-Ground Person Re-identification | [Paper](https://link.springer.com/chapter/10.1007/978-981-95-3393-0_42) | <img src="assets/frameworks/pdpa.png" width="320" alt="Perspective Driven Prototype Alignment for Aerial-Ground Person Re-identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://link.springer.com/content/pdf/10.1007/978-981-95-3393-0_42) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **Drones 2025** | UAGRPG | Unsupervised Aerial-Ground Re-Identification from Pedestrian to Group for UAV-Based Surveillance | [Paper](https://www.mdpi.com/2504-446X/9/4/244) | <img src="assets/frameworks/uagrpg.png" width="320" alt="Unsupervised Aerial-Ground Re-Identification from Pedestrian to Group for UAV-Based Surveillance — Figure 2"><br><sub>Original paper figure: [Figure 2](https://mdpi-res.com/d_attachment/drones/drones-09-00244/article_deploy/drones-09-00244-v2.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://creativecommons.org/licenses/by/4.0/)</sub> |
| **自动化学报 2025** | — | Implicit Decoder Alignment for Aerial-ground Person Re-identification | [Paper](https://www.aas.net.cn/cn/article/doi/10.16383/j.aas.c240705) | <img src="assets/frameworks/implicit-decoder-alignment.png" width="320" alt="Implicit Decoder Alignment for Aerial-ground Person Re-identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://www.aas.net.cn/cn/article/pdf/preview/10.16383/j.aas.c240705.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **CVPR 2024** | VDT | View-decoupled Transformer for Person Re-identification under Aerial-ground Camera Network | [Paper](https://arxiv.org/abs/2403.14513) · [Code](https://github.com/LinlyAC/VDT-AGPReID?tab=readme-ov-file) | <img src="assets/frameworks/vdt.png" width="320" alt="View-decoupled Transformer for Person Re-identification under Aerial-ground Camera Network — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2403.14513v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **TITS 2024** | V2E | Bridging Aerial and Ground Views for Person Re-identification | [Paper](https://arxiv.org/abs/2401.02634) · [Code](https://github.com/huynguyen792/AG-ReID.v2) | <img src="assets/frameworks/v2e.png" width="320" alt="Bridging Aerial and Ground Views for Person Re-identification — Figure 9"><br><sub>Original paper figure: [Figure 9](https://arxiv.org/pdf/2401.02634v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ICME 2023** | Explain | Aerial-Ground Person Re-ID | [Paper](https://arxiv.org/abs/2303.08597) | <img src="assets/frameworks/explain.png" width="320" alt="Aerial-Ground Person Re-ID — Figure 4"><br><sub>Original paper figure: [Figure 4](https://arxiv.org/pdf/2303.08597v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ATR 2017** | — | Person Re-Identification Across Aerial and Ground-Based Cameras by Deep Feature Fusion | [Paper](https://publica.fraunhofer.de/bitstreams/ef904224-f31f-484d-b8d2-56695e46779c/download) | <img src="assets/frameworks/deep-feature-fusion.png" width="320" alt="Person Re-Identification Across Aerial and Ground-Based Cameras by Deep Feature Fusion — Figure 2"><br><sub>Original paper figure: [Figure 2](https://publica.fraunhofer.de/bitstreams/ef904224-f31f-484d-b8d2-56695e46779c/download) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |

### Image-based Vehicle AG-ReID

| Conference / Journal | Method | Title | Resources | Framework |
| :------------------- | :----- | :----------------------------------------------------------------------------------- | :------------------------------------------------- | :---: |
| **SENSORS 2025** | CVNet | Lightweight Cross-View Vehicle ReID with Multi-Scale Localization | [Paper](https://www.mdpi.com/1424-8220/25/9/2809) | <img src="assets/frameworks/cvnet.png" width="320" alt="Lightweight Cross-View Vehicle ReID with Multi-Scale Localization — Figure 3"><br><sub>Original paper figure: [Figure 3](https://mdpi-res.com/d_attachment/sensors/sensors-25-02809/article_deploy/sensors-25-02809-v2.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://creativecommons.org/licenses/by/4.0/)</sub> |
| **RS 2025** | AGID | Aerial-Ground Cross-View Vehicle Re-Identification: A Benchmark Dataset and Baseline | [Paper](https://www.mdpi.com/2072-4292/17/15/2653) | <img src="assets/frameworks/agid.png" width="320" alt="Aerial-Ground Cross-View Vehicle Re-Identification: A Benchmark Dataset and Baseline — Figure 4"><br><sub>Original paper figure: [Figure 4](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-17-02653/article_deploy/remotesensing-17-02653-v2.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://creativecommons.org/licenses/by/4.0/)</sub> |

### Video-based Person AG-ReID

| Conference / Journal | Method | Title | Resources | Framework |
| :------------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **WACVW 2026** | SAS-VPReID | A Scale-Adaptive Framework with Shape Priors for Video-based Person Re-Identification at Extreme Far Distances | [Paper](https://arxiv.org/pdf/2601.05535) · [Code](https://github.com/YangQiWei3/SAS-VPReID) | <img src="assets/frameworks/sas-vpreid.png" width="320" alt="A Scale-Adaptive Framework with Shape Priors for Video-based Person Re-Identification at Extreme Far Distances — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2601.05535v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **WACVW 2026** | S3-CLIP | Video Super Resolution for Person-ReID | [Paper](https://arxiv.org/abs/2601.08807) · [Code](https://github.com/TomasDelaney/S3-CLIP) | <img src="assets/frameworks/s3-clip.png" width="320" alt="Video Super Resolution for Person-ReID — Figure 1"><br><sub>Original paper figure: [Figure 1](https://arxiv.org/pdf/2601.08807v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **WACVW 2026** | EAGLE-ReID | Strategic alignment and delta consistency for extreme far-distance aerial-ground re-identification | [Paper](https://openaccess.thecvf.com/content/WACV2026W/VReID-XFD/html/Kang_EAGLE-ReID_Strategic_Alignment_and_Delta_Consistency_for_Extreme_Far-Distance_Aerial-Ground_WACVW_2026_paper.html) | <img src="assets/frameworks/eagle-reid.png" width="320" alt="Strategic alignment and delta consistency for extreme far-distance aerial-ground re-identification — Figure 3"><br><sub>Original paper figure: [Figure 3](https://openaccess.thecvf.com/content/WACV2026W/VReID-XFD/papers/Kang_EAGLE-ReID_Strategic_Alignment_and_Delta_Consistency_for_Extreme_Far-Distance_Aerial-Ground_WACVW_2026_paper.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **WACVW 2026** | — | Enhancing Aerial–Ground Video Person Re-Identification via DFGS-Guided  CLIP Sampling and Inference-Time Uncertainty-Aware Fusion | [Paper](https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C45&q=Enhancing+Aerial%E2%80%93Ground+Video+Person+Re-Identification+via+DFGS-Guided++CLIP+Sampling+and+Inference-Time+Uncertainty-Aware+Fusion&btnG=) | <img src="assets/frameworks/dfgs-clip.png" width="320" alt="Enhancing Aerial-Ground Video Person Re-Identification via DFGS-Guided CLIP Sampling and Inference-Time Uncertainty-Aware Fusion — Figure 1"><br><sub>Original paper figure: [Figure 1](https://openaccess.thecvf.com/content/WACV2026W/VReID-XFD/papers/Nguyen_Enhancing_Aerial-Ground_Video_Person_Re-Identification_via_DFGS-Guided_CLIP_Sampling_and_WACVW_2026_paper.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **CVPR 2025** | AG-VPReID | A Challenging Large-Scale Benchmark for Aerial-Ground Video-based Person Re-Identification | [Paper](https://arxiv.org/abs/2503.08121) | <img src="assets/frameworks/ag-vpreid.png" width="320" alt="A Challenging Large-Scale Benchmark for Aerial-Ground Video-based Person Re-Identification — Figure 3"><br><sub>Original paper figure: [Figure 3](https://arxiv.org/pdf/2503.08121v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **IJCB 2025** | VM-TAPS | View-specific Memory with Temporal and Scale Awareness Framework for Video-based Cross-View Person Re-Identification | [Paper](https://www.di.ubi.pt/%7Ehugomcp/doc/rashid_ijcb2025.pdf) · [Code](https://github.com/MdRashidunnabi/VM-TAPS) | <img src="assets/frameworks/vm-taps.png" width="320" alt="View-specific Memory with Temporal and Scale Awareness Framework for Video-based Cross-View Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://www.di.ubi.pt/~hugomcp/doc/rashid_ijcb2025.pdf) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner</sub> |
| **TBIOM 2025** | DetReIDX | A Stress-Test Dataset for Real-World UAV-Based Person Recognition | [Paper](https://arxiv.org/pdf/2505.04793) | <img src="assets/frameworks/detreidx.png" width="320" alt="A Stress-Test Dataset for Real-World UAV-Based Person Recognition — Figure 5"><br><sub>Original paper figure: [Figure 5](https://arxiv.org/pdf/2505.04793v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **TBIOM 2025** | MTF–CVReID | Seeing Across Time and Views: Multi-Temporal Cross-View Learning for Robust Video Person Re-Identification | [Paper](https://arxiv.org/pdf/2511.02564) · [Code](https://github.com/MdRashidunnabi/MTF-CVReID) | <img src="assets/frameworks/mtf-cvreid.png" width="320" alt="Seeing Across Time and Views: Multi-Temporal Cross-View Learning for Robust Video Person Re-Identification — Figure 2"><br><sub>Original paper figure: [Figure 2](https://arxiv.org/pdf/2511.02564v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |
| **ECCV 2024** | — | Cross-Platform Video Person ReID: A New Benchmark Dataset and Adaptation Approach | [Paper](https://arxiv.org/abs/2408.07500) · [Code](https://github.com/FHR-L/VSLA-CLIP) | <img src="assets/frameworks/cross-platform-video.png" width="320" alt="Cross-Platform Video Person ReID: A New Benchmark Dataset and Adaptation Approach — Figure 3"><br><sub>Original paper figure: [Figure 3](https://arxiv.org/pdf/2408.07500v1) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner · [License](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html)</sub> |

---

### Challenges & Workshops

| Conference / Journal | Title                                                                                     | Resources                                                                            |
| :------------------- | :---------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **WACV 2026**        | VReID-XFD: Video-based Object Re-identification at Extreme Far Distance Challenge Results | [Paper](https://arxiv.org/pdf/2601.01312v1)                                          |
| **IJCB 2025**        | AG-VPReID 2025: Aerial-Ground Video-based Object Re-identification Challenge Results      | [Paper](https://arxiv.org/pdf/2506.22843)                                            |
| **IJCB 2023**        | AG-ReID 2023: Aerial-Ground Object Re-identification Challenge Results                    | [Paper](https://cvlab.cse.msu.edu/pdfs/IJCB_AG_ReID2023_Challenge_Summary_Paper.pdf) |

---


## 💾 Datasets

Statistics are taken from the dataset papers; A/G/W denote aerial, ground, and wearable cameras.

| Dataset | Source | IDs | Images | Data | Scenes | Cameras | Attributes | Captions | Illumination | Cross-Time | Season | Altitude | Download |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AG-ReID** | ICME 2023 | 388 | 21983 | real | 1 | 2 (1A+1G) | 15 | × | Day | × | Spring, Summer | 15–45 m | [Link](https://drive.google.com/file/d/1hzieEPlXfjkN3V3XWqI5rAwpF_sCF1K9/view) |
| **AG-ReID.v2** | TITS 2024 | 1615 | 100502 | real | 1 | 3 (1A+1G+1W) | 15 | × | Day | × | Spring, Summer | 1.5 m, 3 m, 15–45 m | [Link](https://drive.google.com/drive/folders/16r7G_CuUqfWG6_UCT7goIGRMqJird6vK) |
| **CARGO** | CVPR 2024 | 5000 | 108563 | synthetic | 1 | 13 (5A+8G) | 0 | × | Day & Night | × | Virtual Summer | 5–75 m | [Link](https://drive.google.com/file/d/1yDjyH0VtW7efxP3vgQjIqTx2oafCB67t/view) |
| **G2APS-ReID** | CVPR 2025 | 2788 | 200864 | real | 1 | 2 (1A+1G) | 0 | × | Day or Night | × | Summer | 20–60 m | [Link](https://pan.baidu.com/share/init?surl=MRrhqoQzwxw7qOx4Lqdl2g) |
| **LAGPeR** | CVPR 2025 | 4231 | 63842 | real | 7 | 21 (7A+14G) | 0 | × | Day or Night | × | Summer | 20–60 m | [Link](https://pan.baidu.com/share/init?surl=MRrhqoQzwxw7qOx4Lqdl2g) |
| **CP2108** | AAAI 2026 | 2108 | 142817 | real | 8 | 39 (17A+22G) | 22 | ✓ | Day & Night | ✓ | All Year | 2 m, 15–60 m | [Link](https://github.com/ahu-xhao/SVPR-ReID) |

#### Other related datasets

| Dataset | Source | Category | Download |
| :--- | :--- | :--- | :--- |
| **MOO** | ArXiv 2026 | Image.Animal | [Link](https://github.com/TurtleSmoke/MOO) |
| **AG-VPReID** | CVPR 2025 | Video.Person | [Link](https://drive.google.com/drive/folders/1wtdhKzK9Fbj7xkGAM84KNJ1uYCxSMHdj) |
| **DetReIDX** | TBIOM 2025 | Video.Person | [Link](https://github.com/kailashhambarde/DetReIDX/tree/main) |

### Current SOTA on the first five public benchmarks

Verified on **2026-10-02** from reported standard protocols. For each protocol, the method is selected by the highest reported mAP; the paired value is that same method's **mAP / Rank-1 (%)** (so Rank-1 is not necessarily the standalone maximum). Results have not been independently reproduced.

| Dataset | Method(s) | Standard-protocol result (mAP / Rank-1) | Source |
| :--- | :--- | :--- | :--- |
| **AG-ReID** | GLPSG | A→G: 81.50 / 87.70; G→A: 84.30 / 90.60 | [GLPSG](https://link.springer.com/chapter/10.1007/978-981-95-5755-4_7) |
| **AG-ReID.v2** | HiHR; CVAF | A→C: 84.04 / 88.84 (HiHR); C→A: 83.21 / 88.57 (HiHR); A→W: 87.81 / 92.49 (CVAF); W→A: 85.08 / 90.85 (CVAF) | [HiHR](https://arxiv.org/abs/2607.09186) · [CVAF](https://dl.acm.org/doi/10.1145/3785482) |
| **CARGO** | HiHR; MCVL; ViSA | ALL: 67.52 / 74.36 (HiHR); A→G: 70.53 / 75.53 (HiHR); A→A: 72.41 / 82.50 (MCVL); G→G: 83.90 / 88.39 (ViSA) | [HiHR](https://arxiv.org/abs/2607.09186) · [MCVL](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/7411.pdf) · [ViSA](https://arxiv.org/abs/2605.18192) |
| **G2APS-ReID** | MCVL | A→G: 62.95 / 78.87; G→A: 59.70 / 74.50 | [MCVL](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/7411.pdf) |
| **LAGPeR** | HiHR | A→G: 33.80 / 46.95; G→A: 36.74 / 39.30; G→A+G: 23.99 / 31.39 | [HiHR](https://arxiv.org/abs/2607.09186) |

---

### More Related Exploration

| Conference / Journal | Title                                                                                                                   | Resources                                                                                                                                                                                     |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ArXiv 2025**       | Multi-modal Multi-platform Person Re-Identification: Benchmark and Method                                               | [Paper](https://arxiv.org/pdf/2503.17096) · [Code](https://github.com/MP-ReID/mp-reid) · [Dataset](https://drive.google.com/file/d/1hImLEMcsBB2kNV4McGyksVAumLjZQoUU/view)                    |
| **TCSVT 2025**       | AEA-FIRM: Adaptive Elastic Alignment with Fine-Grained Representation Mining for Text-based Aerial Pedestrian Retrieval | [Paper](https://ieeexplore.ieee.org/document/11072214) · [Code](https://github.com/xbdxwyh/AEA-FIRM-main) · [Dataset](https://drive.google.com/file/d/1YYIpBDoJzTIwYRlpWUqEHmpo5GK05S_W/view) |
| **IJCB 2025**        | AG-VPReID.VIR: Bridging Aerial and Ground Platforms for Video-based Visible-Infrared Person Re-ID                       | [Paper](https://arxiv.org/abs/2507.17995) · [Dataset](https://drive.google.com/drive/folders/1Iy814PqWjwIZcv6CZpieFju-Dop9Y2G7)                                                               |
| **SPL 2025**         | Omni-Directional View Person Re-Identification Through 3D Human Reconstruction                                          | [Paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10839551)                                                                                                                    |
| **ACM MM 2024**      | AerialGait: Bridging Aerial and Ground Views for Gait Recognition                                                       | [Paper](https://dl.acm.org/doi/pdf/10.1145/3664647.3681002)                                                                                                                                   |

---

## 🤖 Automatic Paper Tracking

This repository can search arXiv, OpenAlex, Crossref and DBLP every week, deduplicate the results, and open a rolling review issue. Search results are **never added to the curated list automatically**. After human approval, a manual workflow creates a pull request that updates both README files.

See the [Chinese setup and review guide](docs/PAPER_TRACKER.zh-CN.md).

---

## 📈 Star History
<picture>
  <source media="(prefers-color-scheme: dark)"
    srcset="https://api.star-history.com/svg?repos=YangQiWei3/Awesome-Aerial-Ground-Object-Re-Identification&type=Date&theme=dark" />
  <source media="(prefers-color-scheme: light)"
    srcset="https://api.star-history.com/svg?repos=YangQiWei3/Awesome-Aerial-Ground-Object-Re-Identification&type=Date" />
  <img alt="Star History Chart"
    src="https://api.star-history.com/svg?repos=YangQiWei3/Awesome-Aerial-Ground-Object-Re-Identification&type=Date" />
</picture>


---

## 🤝 Contributing

PRs / Issues are welcome! Please follow these rules:

1. Add your entry to the correct section (Papers / Challenges / Datasets).
2. Keep tables sorted by **Year (desc)**, then **Venue**.
3. Formatting:

   * Venue in **bold** (e.g., `**CVPR 2025**`)
   * Use `—` if method is unknown
   * Resource order: `Paper · Code · Dataset · Project` (only include available links)
   * Core-paper entries must use an author-original figure from a pinned official PDF. Add its metadata to `data/frameworks.json`, crop it with `python scripts/extract_frameworks.py PAPER_ID`, and regenerate both README files with `python scripts/update_readmes.py`.
   * Cropping may remove page whitespace only. Do not redraw, recolor, annotate, or substitute a third-party/AI-generated diagram.

**Template**

```markdown
| **VENUE YEAR** | Method | Paper Title | [Paper](link) · [Code](link) · [Dataset](link) · [Project](link) | Author-original Figure |
```


---

## 🤝 Acknowledgments

We express our sincere gratitude to the academic community and all researchers contributing to the advancement of Aerial-Ground Object Re-Identification.

## 📧 Contact

Questions, suggestions and collaborations are welcome. Please feel free to reach out:

- **Email**: [dutyqw@mail.dlut.edu.cn](mailto:dutyqw@mail.dlut.edu.cn)
- **GitHub**: [Yang Qiwei](https://github.com/YangQiWei3)

## 📌 Citation

If you find our work or this repository useful in your research, please consider citing:

```bibtex
@misc{yang2026hihr,
  title         = {HiHR: Hierarchical Hyperbolic Representation for Aerial-Ground Person Re-Identification},
  author        = {Qiwei Yang and Pingping Zhang},
  year          = {2026},
  eprint        = {2607.09186},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CV},
  url           = {https://arxiv.org/abs/2607.09186}
}

@article{yang2026sas,
  title={SAS-VPReID: A Scale-Adaptive Framework with Shape Priors for Video-based Person Re-Identification at Extreme Far Distances},
  author={Yang, Qiwei and Zhang, Pingping and Wang, Yuhao and Gong, Zijing},
  journal={arXiv preprint arXiv:2601.05535},
  year={2026}
}

@article{wang2025sd,
  title={SD-ReID: View-aware Stable Diffusion for Aerial-Ground Person Re-Identification},
  author={Wang, Yuhao and Hu, Xiang and Wang, Lixin and Zhang, Pingping and Lu, Huchuan},
  journal={arXiv preprint arXiv:2504.09549},
  year={2025}
}

@article{zhang2025latex,
  title={Latex: Leveraging attribute-based text knowledge for aerial-ground person re-identification},
  author={Zhang, Pingping and Hu, Xiang and Wang, Yuhao and Lu, Huchuan},
  journal={arXiv preprint arXiv:2503.23722},
  year={2025}
}

@misc{awesome_agpreid,
  title        = {Awesome Aerial-Ground Object Re-Identification},
  author       = {Yang, Qiwei, Zhang, Pingping and Gong, Zijing},
  howpublished = {\url{https://github.com/YangQiWei3/Awesome-Aerial-Ground-Object-Re-Identification}},
  year         = {2026},
  note         = {A curated list of papers, datasets, and resources for AGPReID.}
}
```
