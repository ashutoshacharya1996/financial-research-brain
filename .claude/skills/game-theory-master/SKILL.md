---
name: game-theory-master
description: |
  Applies game theory to any real-world situation — personal, professional, financial, or social.
  Trigger whenever the user asks: "What's my best move?", "How do I handle this?", "What will
  they do if I do X?", "How do I negotiate this?", "Should I cooperate or compete?", "What's
  the optimal strategy here?" Also trigger for salary negotiation, office politics, pricing,
  vendor/client dynamics, co-founder disputes, competition analysis, or any decision where
  outcome depends on other people's choices. Trigger for: "apply game theory", "think about
  this strategically", "what's the equilibrium", "how will this play out", "what are they
  thinking". Lead with ELI15. Always identify game type first — it changes the entire strategy.
model: sonnet
---

# Game Theory Master Skill

## The Core Mental Model

Game theory is not about winning at board games. It's about making optimal decisions when the outcome depends not just on what *you* do, but on what *other intelligent actors* do.

**The fundamental shift:** Stop asking "What should I do?" and start asking "What is the best response to what they will rationally do, given what they expect me to do?"

**The Golden Rule (non-negotiable):** Always assume the other player is as smart as you. If your plan requires them to be stupid or oblivious, it's not strategy — it's a gamble.

---

## Non-Negotiable Rules

- Always ELI15 first. Translate every concept before using it.
- Identify game type BEFORE recommending strategy. Wrong game type = wrong strategy.
- Complete all 5 stages in order. Do not skip to recommendations.
- Never output a move without first asking: "What does the other player gain by countering this?"
- If a situation has more than 3 players, flag coalition dynamics explicitly.
- Behavioral deviations (emotions, irrationality, spite) must be modeled — not ignored.
- If payoffs are asymmetric or unclear, surface that first. The hardest part is knowing what people actually want, not computing the equilibrium.
- Every recommendation must include: the move, the reasoning, the counter-risk, and the exit.

---

## Stage 1 — Situation Decomposition

Before any analysis, extract the raw structure of the "game."

### 1A. Identify the Players

| Question | What to Find |
|---|---|
| Who has a decision to make? | All active players — including silent ones |
| Who are the observers? | Third parties whose reactions change payoffs (audiences, referees, the market) |
| Are players monolithic or fragmented? | A "company" may have a CEO, board, and HR all with different payoffs |
| Who has no seat but affects the game? | Regulators, public opinion, time itself |

**Flag:** If a player's true identity is unclear, surface the ambiguity. A negotiation with "HR" is really a negotiation with a person who answers to a manager who has a budget.

### 1B. Map the Payoffs

Payoff = what each player is *actually* optimizing for. This is rarely what they say.

| Stated Goal | Likely Real Payoff |
|---|---|
| "We want a fair deal" | Protecting margin / not setting a precedent |
| "We're just looking for the right fit" | Risk reduction / not making a mistake they answer for |
| "I just want what's fair" | Face-saving + avoiding the appearance of losing |
| "We want a long-term partnership" | Locking in favorable terms before you get stronger |

**Payoff currencies (not just money):**
- Time and cognitive load
- Status and reputation (internal and external)
- Optionality (keeping future choices open)
- Risk reduction (avoiding blame, avoiding loss)
- Relationship capital (with the person, or via them)
- Precedent (this deal sets the template for the next one)

**ELI15:** Payoffs are like "what score they're keeping." Figure out what game they think they're playing before you decide how to play yours.

### 1C. List All Strategies

Enumerate the realistic moves for each player. Not every possible move — the plausible ones.

For each player: What are their 2-4 realistic options right now?

Then for each combo of moves, ask: What outcome does each combination produce? This is the payoff matrix. You don't need to write it all out — you need to internalize it.

---

## Stage 2 — Game Type Classification

**This is the most critical step.** The game type determines which strategies are valid. Getting this wrong means applying the wrong playbook.

### Game Type Decision Tree

```
Is there a fixed total to divide?
  YES -> Zero-Sum game -> Go to 2A
  NO  -> Can both sides win together?
          YES -> Non-Zero-Sum -> Go to 2B
          NO  -> Mixed Motive -> Go to 2C

Do you move simultaneously or take turns?
  Same time  -> Simultaneous -> affects strategy selection
  Take turns -> Sequential   -> use Backwards Induction

Will you interact again?
  Once       -> One-shot  -> be more aggressive / defect is tempting
  Repeatedly -> Iterated  -> cooperation becomes rational
```

### 2A. Zero-Sum Games

**Characteristics:** One player's gain is exactly another's loss. Fixed pie.

**Examples:** Salary negotiation (fixed budget), competitive bidding, price wars.

| Principle | Application |
|---|---|
| Hide your reservation price | Never reveal how low you'll go / how much you need it |
| Create false alternatives | Even credible threats of alternatives shift the equilibrium |
| Claim value, don't create it | Framing, anchoring, and sequencing matter enormously |
| The BATNA principle | Best Alternative To Negotiated Agreement. Your BATNA is your true power. If your BATNA is weak, fix it before negotiating. |

**ELI15:** Imagine you're dividing a pizza. The game is to get more slices. You're not trying to make the pizza bigger — just grab more before the other person does.

### 2B. Non-Zero-Sum (Cooperative / Coordination) Games

**Characteristics:** Joint gains are possible. Both can win — or both can lose.

**Examples:** Project collaboration, partnerships, setting industry standards, peace negotiations.

| Principle | Application |
|---|---|
| Signaling commitment | Show you're invested so they feel safe being invested too |
| Creating value before claiming it | Expand the pie together before fighting over shares |
| Focal points (Schelling points) | In coordination games, people converge on "obvious" solutions. Identify and propose the focal point early. |
| Credible promises | A promise only works if breaking it is costly to you. Make commitments visible and costly to reverse. |

**ELI15:** Now imagine you and a friend are building a bigger pizza together. If you both put in effort, there's more for everyone. But if one person free-rides, the other gets burned and stops trying.

### 2C. Mixed Motive Games (Most Real-World Situations)

Part cooperative, part competitive. You need each other AND you're competing.

The Prisoner's Dilemma is the archetype:

```
              They Cooperate    They Defect
You Coop:     Both win (good)   You lose big
You Defect:   You win big       Both lose (bad)
```

**The trap:** Defecting feels safe (you can't get burned). But if both defect, the outcome is worse for everyone than if both cooperated. This is why trust and credible commitment matter.

**How to escape the Prisoner's Dilemma:**
1. Make defection costly (contracts, reputation, public commitment)
2. Shift to an iterated game (future interactions make cooperation rational)
3. Change payoffs (align incentives so cooperation dominates)
4. Use tit-for-tat (cooperate first, mirror their move immediately after)

### 2D. Game Timing

**Simultaneous moves** (neither player sees the other's move first):
- Think about what they expect you to do, then decide
- Mixed strategies (randomizing) can prevent exploitation
- Look for dominant strategies (moves that win regardless of what they do)

**Sequential moves** (one player acts, then the other responds):
- Use Backwards Induction: start from the end state and work backwards
- First-mover advantage exists when commitment matters more than information
- Second-mover advantage exists when information matters more than commitment

---

## Stage 3 — Equilibrium Analysis

### 3A. Dominant Strategy Search

A dominant strategy wins regardless of what the other player does.

Check: "Is there a move that beats (or ties) every possible response from the other side?" If yes, that's the answer. Play it. Stop analyzing.

If no dominant strategy exists, proceed to Nash Equilibrium.

### 3B. Nash Equilibrium

The Nash Equilibrium is the stable outcome where:
- Given what you're doing, they have no reason to change
- Given what they're doing, you have no reason to change

**How to find it:** For each of their strategies: what's your best response? For each of your strategies: what's their best response? The intersection is the Nash Equilibrium.

**Important caveat:** Nash Equilibrium is stable — not necessarily good. The Prisoner's Dilemma equilibrium is mutual defection. Stable, but bad for both. This is why changing the game (mechanism design) is sometimes the right move.

### 3C. Multiple Equilibria Problem

When there are multiple equilibria, the question becomes: which one do you land on?

**Coordination tools:**
- Announce your intent publicly (Schelling focal point)
- Go first and commit credibly (first-mover locks the equilibrium)
- Use precedent ("we've always done it this way")
- Find the "obvious" answer both sides can see without communicating

### 3D. Mixed Strategy Equilibrium

When no pure strategy equilibrium exists, the optimal play is to randomize.

**When this applies:** When your opponent will exploit any predictable pattern. Examples: Penalty kicks in football, bluffing in poker, surprise inspections.

**ELI15:** If you always kick left on penalties, the goalkeeper learns to dive left. So you mix it up to stay unpredictable. The math tells you the exact ratio to randomize.

---

## Stage 4 — Advanced Mechanics (Apply When Relevant)

Load these modules based on the situation. Not all apply every time.

### 4A. Information Asymmetry

**Applies when:** One player knows something the other doesn't.

| Situation | Who Has the Edge | Strategy |
|---|---|---|
| Selling (you know the product's flaws) | Seller | Buyer: demand signals, warranties, trials |
| Job interview (you know your weaknesses) | Candidate | Employer: structured tests, reference checks |
| Negotiation (you know your walkaway price) | Party with hidden info | Other side: anchoring, fake deadlines, silence |

**Signaling:** Sending credible information about hidden qualities. Only works if the signal is costly to fake. A degree signals intelligence partly because it's too hard for unintelligent people to fake.

**Screening:** Designing a mechanism that causes people to reveal their type. Example: Insurance deductibles. If you choose high deductible, you signal you're low-risk.

### 4B. Mechanism Design ("Reverse Game Theory")

Standard game theory asks: given these rules, what will people do? Mechanism design asks: what rules should we create to produce the outcome we want?

**Apply when:** You have the power to set the structure of the interaction.

Examples:
- Setting auction rules to maximize revenue
- Designing compensation structures to align incentives
- Structuring a deal so both parties are better off cooperating
- Creating a policy that makes the right behavior the rational behavior

**The Revelation Principle:** A well-designed mechanism makes it rational for everyone to just tell the truth. You don't need to trick people — design the game so honesty dominates.

### 4C. Repeated Games and Reputation

In one-shot games, defection is tempting. In repeated games, cooperation can be rational.

**The Folk Theorem:** In infinitely repeated games, almost any outcome (including full cooperation) can be sustained as an equilibrium — if players value the future enough.

**The discount factor:** How much do future payoffs matter? If someone doesn't care about the relationship after this interaction, they'll defect. If they do care, cooperation is stable.

**Tit-for-Tat:** The robust strategy in iterated Prisoner's Dilemmas:
1. Cooperate on the first move
2. Do exactly what they did last round
3. Never hold a grudge (forgive one period of defection)
4. Be transparent — let them see your strategy so they know what to expect

**Reputation as capital:** In repeated interactions with different partners, your reputation is an asset. Defecting once pays off short-term but destroys future value.

### 4D. Coalition and Multi-Player Dynamics

When there are 3+ players, alliances form. The game becomes about inclusion and exclusion.

| Principle | Application |
|---|---|
| The pivotal player has power | The person who makes a coalition succeed or fail sets the price |
| Coalitions are fragile | Any member can defect if offered more by the other side |
| Exclude to create urgency | Threatening to form a coalition without someone changes their calculus |
| The minimum winning coalition | Don't offer more partners than you need — the value divides further |

### 4E. Behavioral Deviations (When Rational Models Break)

Real people are not rational. These deviations are predictable and exploitable.

| Bias | What It Causes | Strategic Implication |
|---|---|---|
| Loss aversion | Losses feel 2x worse than equivalent gains | Frame offers as "avoiding a loss" not "gaining something" |
| Anchoring | First number heard distorts all subsequent judgment | Set the anchor aggressively and early |
| Reciprocity | People feel compelled to return favors | Give something small first to create obligation |
| Status quo bias | Inertia toward current situation | Make your proposal the default, not the alternative |
| Sunk cost fallacy | Can't let go of past investments | Use against others: remind them how much they've invested |
| Fairness norms | People reject "unfair" offers even at their expense | A bad deal framed as unfair gets rejected. A same deal framed as fair gets accepted. |
| Overconfidence | People think they'll win more than they will | Let them pitch to you. Overconfident people reveal their cards. |

---

## Stage 5 — Output: The Strategic Recommendation

Use this structure for every final output:

```
GAME THEORY ANALYSIS — [Situation Name]
Date: [date]

ELI15 SUMMARY
[2-3 sentences. No jargon. What is actually happening here?]

THE GAME
Players: [list all, including silent ones]
Game type: [Zero-sum / Non-zero-sum / Mixed motive + Simultaneous/Sequential + One-shot/Repeated]
Key information asymmetries: [who knows what the other doesn't]

THE PAYOFFS (what they're actually optimizing for)
Player A: [real payoff, not stated goal]
Player B: [real payoff, not stated goal]
[etc.]

EQUILIBRIUM ANALYSIS
Dominant strategy (if exists): [move + reasoning]
Nash Equilibrium: [stable outcome if both play rationally]
Risk of multiple equilibria: [yes/no — if yes, which one are you likely to land on?]

BEHAVIORAL WILDCARDS
[List 2-3 predictable irrational behaviors that could shift the outcome]

THE RECOMMENDED MOVE
Move: [specific action]
Why it's optimal: [logic]
What it assumes about them: [stated assumption]
Counter-risk: [what happens if they respond unexpectedly]
Exit: [what you do if this doesn't work]

MECHANISM DESIGN OPTION (if applicable)
[Can you change the rules of the game itself? If yes, how?]

WATCHPOINTS
If [X happens] -> shift to [Y strategy]
If [X happens] -> shift to [Y strategy]

BEHAVIORAL FLAGS (for the user)
[Any biases the user might be carrying into this situation that could distort their play]
```

---

## Quick Reference: Game Type -> Strategy Mapping

| Game Type | Optimal Strategy |
|---|---|
| Zero-sum, one-shot | Protect BATNA, anchor first, hide reservation price |
| Zero-sum, repeated | Tit-for-tat, protect reputation, signal credibly |
| Non-zero-sum, coordination | Signal commitment, find focal point, create value first |
| Non-zero-sum, Prisoner's Dilemma | Change payoffs, make defection costly, use iterated framing |
| Sequential, you go first | Commit credibly to lock the equilibrium in your favor |
| Sequential, they go first | Wait for information, then respond optimally |
| Information asymmetry (you have info) | Signal via costly actions |
| Information asymmetry (they have info) | Screen via mechanism design |
| Multi-player / coalition | Identify the pivotal player, exploit fragile alliances |
| Irrational opponent | Model their specific bias, don't assume rationality |

---

## Real-World Application Library

Load these when the situation matches. These are worked examples to calibrate output quality.

### Salary Negotiation
**Game:** Zero-sum (fixed budget) + Information asymmetry (they know the band, you don't)
**Key move:** Strengthen your BATNA before the conversation. A competing offer changes everything. Anchor high, let them move you down — whoever moves first loses ground. Never reveal your current salary (it anchors their offer downward). Make the conversation about market rate, not about you personally.

### Office Politics / Internal Competition
**Game:** Repeated, mixed motive, multi-player
**Key move:** Tit-for-tat. Be visibly cooperative. Mirror defection immediately and visibly. Build coalitions with pivotal players. Never attack directly — change the game structure instead. Your reputation is a long-horizon asset. Short-term defection is almost never worth it.

### Vendor / Client Negotiation
**Game:** Mixed motive, repeated (if ongoing relationship), sequential
**Key move:** Expand value before dividing it. "How can we both win more?" before "who gets what." Identify which party needs this deal more (weaker BATNA). That party should concede more. Use the "walk away" signal sparingly but credibly. An empty threat destroys credibility forever.

### Competitive Business Strategy
**Game:** Zero-sum (market share) overlaid on non-zero-sum (industry growth)
**Key move:** Sometimes you want the whole industry to grow (cooperate on standards, grow the pie) and compete on execution. Know when you're playing which game. Commitment devices (capacity investments, public promises) deter competitors by changing their expected payoff from entering.

### Relationship / Personal Conflicts
**Game:** Repeated, non-zero-sum, behavioral deviations are dominant
**Key move:** Loss aversion and fairness norms dominate rational play here. Frame offers as loss-avoidance. Invoke shared identity. Reciprocity is powerful. The goal is usually not winning — it's preserving the relationship while resolving the conflict. Tit-for-tat works. Public commitment to a resolution changes the equilibrium.

---

## What This Skill Does NOT Do

- Predict human behavior with certainty — it maps probabilities and structures, not guarantees
- Replace domain-specific expertise (legal, financial, psychological)
- Work when the "game" is purely internal (no other player) — that's a decision theory problem, not game theory
- Provide ethical validation — a strategy can be optimal and still wrong. That's the user's call.
- Guarantee a "win" — game theory finds the best available move, not a guaranteed outcome
- Skip the ELI15 step — every output must be understandable to a non-expert

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This agent synthesises across sources, weighs ambiguous evidence, or produces human-facing
output — requires strong instruction-following and reasoning.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
