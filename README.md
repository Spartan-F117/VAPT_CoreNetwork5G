**Security Analysis of 5G Core Network**
*M.Sc Thesis in Cybersecurity of University of Pisa*

*Abstract:*

The fifth generation of mobile networks defined by 3GPP introduces improvements in every respect over previous ones: bandwidth, latency, security, new use cases and more. The new standard introduces a new architecture in the Core Network, the Service-Based Architecture (SBA), and a new method of intercommunication between the functions (Network Functions) of the Core Network: the Service-Based Interface (SBI). In this new architectural style, each Network Function communicates with the
others through REST API requests (HTTP2/JSON). The mode of communication that is new to telecom technologies has already been established in the realm of web
services, where there are a wide range of vulnerabilities that can be targeted by automated tools. The goal set in this thesis work is to analyze the SBA of the 5G Core and test the security of the API interfaces of Network Functions (NFs) implemented in open-source frameworks, with a hands-on approach, performing API Injection
attacks. The security of the Core Network will also be analyzed by evaluating Network Functions that are reachable from the outside, such as the Access and Mobility
Management Function, assessing resistance to replay and DDoS attacks.

Two widely used open-source implementations of the 5G Core will be explored: **Open Air Interface (OAI)** and **Open5GS**.

This GitHub repository contains traffic captures and results of API injection tests performed during the thesis work.
  
  ```
 ├── API Injection/
    ├── Testset/
        ├── 1. DELETE Subscription ID (Document)/
            ├── oai_test
            └── open5gs_test
        ├── .....
        └── 9. OPTIONS NF INSTANCE (Store)/
            ├── oai_test
            └── open5gs_test
    ├── ts_129510v161300p.pdf
    ├── TS29510_Nnrf_NFManagement_Rel16.yaml
    └── start.py
├── Testbed 1 - Open5GS/
    ├── open5gs.zip
    ├── 5greplay-0.0.1/
        ├── rules/
            ├── nas-smc-replay-attack.so
            └── nas-smc-replay-attack.xml
        ├── 5greplay-sctp.conf
        ├── 5greplay-udp.conf
        └── mmt-5greplay.conf
    ├── CapturedTraffic/
        ├── Result Replay Attack NAS_UE_Auth_open5gs/
            ├── UE_log_replayAttack.txt
            ├── gNB_log_replayAttack.txt
            ├── log_open5gs_replayAttack.txt
            └── log_analysis_replayAttack.pcapng
        ├── NAS_UE_Auth_open5gs.pcapng
        └── ue_authentication.pcapng
    └── Scripts/
        ├── ChangeConfig.sh
        ├── run5gs.sh
        └── stop5gs.sh
├── Testbed 2 - OAI/
    ├── 5greplay-0.0.1/
        ├── rules/
            ├── nas-smc-replay-attack.so
            └── nas-smc-replay-attack.xml
        ├── 5greplay-sctp.conf
        ├── 5greplay-udp.conf
        └── mmt-5greplay.conf
    ├── CapturedTraffic/
        ├── NAS_UE_Auth_OAI.pcapng
        └── ue_authentication.pcapng
    └── Scripts/
        ├── InstallationCoreOAI.sh
        ├── runOAI.sh
        ├── runUERANSIM.sh
        ├── stopOAI.sh
        └── stopUERANSIM.sh
```
