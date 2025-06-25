# OSS-LCAF: Open Source Software License Conflict Analysis Framework

OSS-LCAF is a framework designed to detect and analyze license conflicts in open-source software. This repository contains the **code**, **dataset**, and links to **fine-tuned model adapters** that support the proposed methodology.

## Repository Structure

1. **Code**  
   Contains the full implementation of OSS-LCAF, including preprocessing scripts, model integration, and evaluation pipelines.

2. **Dataset**  
   Provides the benchmark dataset used for training and evaluation. This dataset includes annotated license metadata and conflict scenarios.

3. **Models**  
   Contains links and/or files for the fine-tuned model adapters, specifically:
   - Gemma-2-2b-it
   - Llama-3.2-3B-instruct

> 📄 Each folder contains a dedicated README file. Please refer to those files for detailed usage instructions and requirements.

---

## Citation

If you use OSS-LCAF or any part of this work in your research or projects, please cite the following paper:

```bibtex
@inproceedings{kahol2025oss,
  title={OSS-LCAF: Open-Source Software License Conflict Analysis Framework},
  author={Kahol, Aditya and Tummepalli, Anka Chandrahas and Anish, Preethu Rose},
  booktitle={2025 IEEE/ACM 47th International Conference on Software Engineering: Companion Proceedings (ICSE-Companion)},
  pages={303--314},
  year={2025},
  organization={IEEE}
}
