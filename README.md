# VAPT_CoreNetwork5G
M.Sc Thesis in Cybersecurity of University of Pisa - Test the API of SBA 5G CN

Project Directory Description:


API Injection /
  Testset /
    1. DELETE Subscription ID ( Document ) /
      oai_test
      open5gs_test
    .....
    9. OPTIONS NF INSTANCE ( Store ) /
      oai_test
      open5gs_test
    ts_129510v161300p.pdf
    TS29510_Nnrf_NFManagement_Rel16.yaml
    start.py

  Testbed 1 - Open5GS /
    open5gs . zip
    5 greplay -0.0.1/
      rules /
        nas - smc - replay - attack . so
        nas - smc - replay - attack . xml
        5 greplay - sctp . conf
        5 greplay - udp . conf
      mmt -5 greplay . conf
  CapturedTraffic /
    NAS_UE_Auth_open5gs . pcapng
    ue_authentication . pcapng
 Scripts /
    ChangeConfig . sh
    run5gs . sh
    stop5gs . sh
		


 Testbed 2 - OAI /
  5 greplay -0.0.1/
  rules /
    nas - smc - replay - attack . so
    nas - smc - replay - attack . xml
  5 greplay - sctp . conf
  5 greplay - udp . conf
  mmt -5 greplay . conf
 CapturedTraffic /
  NAS_UE_Auth_OAI . pcapng
  ue_authentication . pcapng
 Scripts /
  InstallationCoreOAI . sh
  runOAI . sh
  runUERANSIM . sh
  stopOAI . sh
  stopUERANSIM . sh
