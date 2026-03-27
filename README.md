# EquiCut v1.0b — Entropy-Based Optimal Cutoff Tool

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://equicut.streamlit.app/)
![License](https://img.shields.io/github/license/marleaugarvie/EquiCut?color=blue)
![Python Version](https://img.shields.io/badge/python-3.9%2B-brightgreen)

**EquiCut** is a specialized tool designed to calculate Shannon entropy ($H$) and equitability ($E$) to determine empirical cut-off points for continuous or ordinal scales.

---

## 📖 Overview
The dichotomization of continuous or ordinal scales is a common practice in psychometric and survey research, but the justification for choosing a specific cut-off point is often weak, especially in the absence of an external criterion. 

> **EquiCut** addresses this challenge by implementing an information-theoretic method based on Shannon’s entropy. The tool first computes the entropy value for a full score distribution, which is then normalized by the number of categories to obtain an equivalent equitability index. 
>
> The optimal cut-off is identified by finding the dichotomized distribution whose equitability index best matches that of the original multi-category distribution, thus preserving its fundamental structural properties.

---

## ✨ Key Features
*   **🎯 Data-Driven:** Uses the intrinsic distribution of your data to find the most informative threshold.
*   **💻 User-Friendly:** Requires no programming knowledge or software installation.
*   **📄 Comprehensive Reporting:** Simply upload a frequency data file (`.txt`) to receive a detailed analysis report.
*   **🔓 Open Science:** Fully open-source, transparent, and reproducible.

---

## 🔗 Project Resources
To facilitate research and implementation, the different components of this project are available across the following platforms:

*   **🚀 Interactive Web Application:** [equicut.streamlit.app](https://equicut.streamlit.app/) — *Run your analysis instantly in the browser.*
*   **📚 Original Peer-Reviewed Article:** [Journal of Psychometric Research](https://dergipark.org.tr/en/pub/jopres/article/1761142) — *Theoretical foundation and validation.*
*   **📝 Methodological Research Note:** [Access on PsyArXiv](https://osf.io/preprints/psyarxiv/29vab) — *Detailed pseudo-code and user guide.*
*   **🗄️ Permanent Archive:** [Access on OSF](https://osf.io/8qrz2) — *Archived source code and validation datasets for long-term reproducibility.*

---

### ✍️ Authors
**Philippe Garvie** & **Jacques Marleau**  
📍 Gatineau, Québec, Canada  
📅 **Date:** 2026-03-27  
⚖️ **License:** [MIT License](https://github.com/marleaugarvie/EquiCut/blob/main/LICENSE)
