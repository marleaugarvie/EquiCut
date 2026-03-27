EquiCut v1.0b

Calculates Shannon entropy (H) and equitability (E) for a list of counts.

(Background): The dichotomization of continuous or ordinal scales is a common
practice in psychometric and survey research, but the justification for choosing a
specific cut-off point is often weak, especially in the absence of an external criterion.
(Tool Presentation): We introduce EquiCut, a free, open-source, and
user-friendly web tool designed to address this challenge. (Methodology): Equi-
Cut implements an information-theoretic method based on Shannon’s entropy. The
entropy value for a score distribution is first computed, and an equivalent equitability
index is obtained by normalizing it by the number of categories. The optimal
cut-off is identified by finding the dichotomized distribution whose equitability index
best matches that of the original multi-category distribution, thus preserving its
structural properties. (Features): The tool requires no programming knowledge
or software installation. Users simply upload a frequency data file, and the tool
provides a comprehensive report. (Availability): The web tool and its full Python
source code are freely available.

"For long-term archival purposes, a stable version of this source code and the associated datasets are also available on OSF at https://osf.io/8qrz2."

Philippe Garvie, Jacques Marleau

Gatineau, Québec, Canada

2026-03-27
