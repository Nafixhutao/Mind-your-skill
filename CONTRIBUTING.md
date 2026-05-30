# Contributing to Mind Your Skill

Thank you for helping improve Mind Your Skill.

This repository is intended to be a curated skill library for Hermes Agent.

## Skill design principles

Skills should be:

- Modular
- Easy to audit
- Safe by default
- Token-aware
- Clear for first-time users
- Useful during repeated runtime use

## Recommended skill structure

Each skill should live under `skills/<skill-name>/`.

```text
skills/<skill-name>/
├─ SKILL.md
├─ README.md
├─ setup.md
├─ runtime.md
├─ examples.md
└─ changelog.md
```

Only include files that are useful for the skill.

## SKILL.md rules

`SKILL.md` should be short. It should act as the entrypoint and router.

It should answer:

- What is this skill for?
- When should Hermes use it?
- Which supporting file should be used for setup or runtime?
- What should the skill avoid doing?

Avoid putting long tutorials, large examples, or implementation details in `SKILL.md`.

## Runtime rules

Runtime instructions should be compact and practical.

A good runtime file should include:

- Intent detection rules
- Minimal parsing rules
- Action/storage behavior
- Response format
- Error handling

Avoid long explanations during runtime.

## Safety rules

Do not hardcode secrets, private tokens, or personal endpoints.

Do not include instructions that exfiltrate user data.

Do not perform destructive actions without clear user intent.

Disclose required permissions in the skill README.

## Registry

When adding a new skill, update `registry.json`.

Use semantic versioning for skill versions when possible.
