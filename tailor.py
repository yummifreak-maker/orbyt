import os
from docx import Document
from config import Config

class ProfileTailor:
    def __init__(self):
        self.base_resume_text = self._load_base_resume()

    def _load_base_resume(self):
        if os.path.exists(Config.RESUME_PATH):
            doc = Document(Config.RESUME_PATH)
            return "\n".join([p.text for p in doc.paragraphs])
        return "M.S. CS ASU, Quantitative Research Experience."

    def generate_cover_letter(self, company_name, job_title, jd_description):
        letter = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} position. As an M.S. Computer Science (AI) graduate from Arizona State University[cite: 1] with hands-on quantitative research experience at A.R.T. Advisors[cite: 1] and a top-4 finish in the WorldQuant Alphathon[cite: 1], I build scalable statistical arbitrage and systematic trading strategies backed by strict point-in-time data handling.

During my time at A.R.T. Advisors, I engineered production pipelines handling over 10 years of ETF data, achieving a 24x speedup and optimizing alpha generation models from a 0.9 to 1.37 Sharpe ratio[cite: 1]. Furthermore, my multi-asset research framework (QuantBook) demonstrates my capacity to bridge data engineering, cross-sectional alpha models, and low-latency execution frameworks (C++ pybind11 OMS)[cite: 1]. 

I hold valid F1 work authorization via STEM OPT through July 2028 and require no sponsorship change immediately. I look forward to contributing analytical rigor and robust engineering to your team at {company_name}.

Sincerely,
{Config.CANDIDATE_NAME}
{Config.USER_EMAIL}
"""
        return letter