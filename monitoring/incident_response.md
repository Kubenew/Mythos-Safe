# Incident Response Playbook

## Severity Levels
- SEV0: confirmed critical harmful capability misuse
- SEV1: probable high-risk exploit
- SEV2: policy violation / jailbreak trend
- SEV3: low-risk bug / false positive

## Immediate Actions
1. Freeze deployments
2. Enable enhanced logging
3. Snapshot model + prompts
4. Notify security owner + legal
5. Run containment checks

## Root Cause Analysis
- Was this a policy gap?
- Was this an eval blind spot?
- Was this a classifier failure?

## Mitigation Options
- Patch refusal policy
- Add classifier rule
- Add RLHF/RLAIF correction
- Retrain targeted SFT set

## Postmortem
- Publish internal report
- Update eval suite
- Update system card
