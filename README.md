# Panning for gold.eth: Understanding and Analyzing ENS Domain Dropcatching
This repository includes the artifacts from the Internet Measurement Conference 2024 paper entitled "Panning for gold.eth: Understanding and Analyzing ENS Domain Dropcatching" by Muhammad Muzammil, Zhengyu Wu, Aruna Balasubramanian, and Nick Nikiforakis [(PDF)](https://www.securitee.org/files/ens_domains_imc2024.pdf).

- all-ens-domains/
    - Contains all collected Ethereum Name Service (ENS) domains collected for the purpose of our work.

- get-ens-domains.py
    - This script collects data from the ENS Subgraph using The Graph's API. It retrieves:
        1. ENS Registrations: Domain registrations, including registration events such as renewals, transfers, and registrant details.
        2. Domain Events: Ownership changes and other events related to ENS domains (Such as Name Wrapping and subdomains).
        3. Domain Names: Basic domain information, including names and their creation dates.

    - Requirements
        1. Python 3.x
        2. requests and logging libraries

    - Running the script:
        - `python3 get-ens-domains.py`

    - Output Structure
        The output consists of JSON files saved in different folders:
        1. registrations/: Contains all ENS domain registration data.
        2. domain-events/: Contains events such as new ownership, transfers, and wrapping.
        3. domains/: Contains domain names and their creation dates.

This collection methodology is also applied in our work **Typosquatting 3.0: Characterizing Squatting in Blockchain Naming Systems** ([(PDF)](https://github.com/pragseclab/ens-dropcatching)).

If you use this work, please use the next citations:

`@inproceedings{muzammil2024expiredens,
  title = {{Panning for gold.eth: Understanding and Analyzing ENS Domain Dropcatching}},
  author = {Muhammad Muzammil and ZhengYu Wu and Aruna Balasubramanian and Nick Nikiforakis},
  booktitle = {Proceedings of the Internet Measurement Conference (IMC)},
  year = {2024},
}

@inproceedings{muzammil2024web3typos,
  title = {{Typosquatting 3.0: Characterizing Squatting in Blockchain Naming Systems}},
  author = {Muhammad Muzammil and ZhengYu Wu and Lalith Harisha and Brian Kondracki and Nick Nikiforakis},
  booktitle = {Proceedings of the Symposium on Electronic Crime Research (eCrime)},
  year = {2024},
}
`
