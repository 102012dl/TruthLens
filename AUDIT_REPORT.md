# TruthLens Audit & Automation Report (WSL Script v3)

Generated: Mon Mar  2 20:41:59 CET 2026

## 1. Repository
- Path: /home/home21id/truthlens
- Git remotes:
gitlab	https://gitlab.com/102012dl/TruthLens.git (fetch)
gitlab	https://gitlab.com/102012dl/TruthLens.git (push)
origin	https://github.com/102012dl/TruthLens.git (fetch)
origin	https://github.com/102012dl/TruthLens.git (push)
- Last commit:
e1deaee docs: add automation audit report for capstone

## 2. Tests
- Pytest status: OK

## 3. Web directory
- web/ status: TRACKED

## 4. Duplicate clones
- truthlens/TruthLens duplicate status: OK

## 5. Remote sync summary
- origin status: IN_SYNC
- gitlab status: IN_SYNC

## 6. Next Steps for Capstone
- Якщо TEST_STATUS=FAILED — переглянь лог pytest вище та виправ тести.
- Якщо WEB_STATUS=UNTRACKED і web/ потрібен у проєкті — додай його в git.
- Якщо ORIGIN_STATUS=DIVERGED — створи бекап-гілку й обережно зроби rebase/merge з origin/main.
- Якщо GITLAB_STATUS=FETCH_FAILED — перевір deploy keys:
  https://gitlab.com/102012dl/TruthLens/-/settings/repository#js-deploy-keys-settings
- Перенеси цей звіт (`AUDIT_REPORT.md`) у Claude Project як технічний артефакт.
