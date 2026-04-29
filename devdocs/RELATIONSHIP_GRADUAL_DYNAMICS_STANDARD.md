# Relationship Gradual Dynamics Standard

FamilyLife reference pattern:

- Daily interaction flags are per-person: talk topics, gift, and flirt reset each day.
- Gifts and flirt are not neutral buttons. They depend on relationship level, the person's current mood, and whether the player has built trust first.
- Weekly chores affect household respect. Good weekly results improve relationship; bad results create anger and reduce future access.
- Bad choices can anger a person and block or penalize later actions until time, apology/talk, or better conduct restores trust.

Tractir implementation:

- `RelationshipDynamics.rpy` is the central gate for social readiness.
- It reads existing authoritative stats: `Friends`, `otkroven`, `sluttiness`, `neshlush`, `TalkedToday`, `GiftedToday`, and Sandra's weekly chore evaluation.
- `talk` remains the safe first step, but anger and rebellion can reduce the score.
- `gift`, `share`, and `flirt` require gradual readiness: talk first, enough friendship/opening, no active anger, and no bad household week blocking trust.
- Bad social results raise anger and `neshlush`; good results calm anger and reduce `neshlush`.
- The weekly chore exam now applies mood consequences through `relationship_apply_weekly_chore_evaluation()`.
- Girl cards show the relationship mood line so the player can see whether someone is distant, trusting, angry, or rebellious.

Adding new social actions:

1. Check `relationship_social_action_allowed(person, action, item_id)` before showing the action.
2. Pass score through `relationship_adjust_social_score(person, action, score)`.
3. Call `relationship_after_social_result(person, action, raw_score, accepted)` after the result.
4. Do not bypass the old stat maps; this layer is a gate and mood modifier, not a replacement for `Friends` or event conditions.
