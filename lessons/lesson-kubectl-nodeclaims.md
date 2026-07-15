# Lesson Plan: Understanding kubectl and NodeClaims (Karpenter)

**Subject:** Kubernetes / Cloud Infrastructure | **Audience:** General audience, no prior experience assumed | **Duration:** 60 minutes
**Setting:** 1-on-1 | **Group size:** 1

---

## Learning Objectives

By the end of this session, participants will be able to:
1. Explain what Kubernetes nodes are and why NodeClaims exist as a resource type (Karpenter's node provisioning mechanism).
2. Apply `kubectl` commands to list, inspect, and describe NodeClaims in a cluster.
3. Interpret the status and lifecycle fields of a NodeClaim to determine whether a node is being provisioned, ready, or being terminated.

**Key vocabulary:** Node, Pod, kubectl, Karpenter, NodeClaim, NodePool, Provisioning

---

## Materials and Preparation

- [ ] A terminal with `kubectl` installed and configured against a test/demo cluster that has Karpenter installed (or a recorded/sandbox cluster if live access isn't available)
- [ ] Screen-share setup so learner can see terminal output clearly
- [ ] A simple diagram (hand-drawn or digital) showing: Pod → NodePool → NodeClaim → Node
- [ ] Sample `kubectl get nodeclaims` and `kubectl describe nodeclaim` output saved as backup in case live cluster is unavailable
- [ ] Room setup: Side-by-side or shared-screen, one terminal, learner has hands-on keyboard access for at least half the session

---

## Lesson Structure

| Time | Phase | Activity | Format |
|---|---|---|---|
| 00:00 | Hook / Opener | Ask: "When you deploy an app to Kubernetes and there's no room for it, where does a new server come from?" Show a live terminal running `kubectl get nodeclaims` on a cluster mid-scale-up, watching a new one appear in real time. | 1-on-1 discussion |
| 00:05 | Prior knowledge | Quick check: "Have you used `kubectl` before? Do you know what a Kubernetes 'node' is?" Adjust pacing based on answer — assume zero knowledge unless stated otherwise. | Q&A |
| 00:10 | Instruction | Explain Kubernetes nodes, then Karpenter, then NodeClaims as the "receipt" for a node request. Use the Pod → NodePool → NodeClaim → Node diagram. | Explanation with diagram |
| 00:25 | Guided practice | Walk through `kubectl get nodeclaims`, `kubectl describe nodeclaim <name>`, and `kubectl get nodeclaims -o wide` together, narrating what each column/field means. | Live demo, learner types commands |
| 00:40 | Independent practice | Learner runs the commands solo on the terminal, describes a NodeClaim, and answers: "Is this NodeClaim ready? How do you know?" | Hands-on task |
| 00:50 | Check for understanding | Ask learner to explain, in their own words, what happens between a Pod being unschedulable and a new Node appearing, using the term NodeClaim correctly. | Verbal explanation |
| 00:55 | Closure | Summarize the Pod → NodePool → NodeClaim → Node flow, preview next-step topics (NodePool config, disruption/consolidation). | Discussion |

---

## Key Explanations and Worked Examples

### What is a Kubernetes Node?
A node is a worker machine (virtual or physical) in a Kubernetes cluster that runs your applications (packaged as Pods). Think of a cluster as an apartment building: each node is a floor with a limited number of rooms (CPU/memory capacity), and Pods are tenants that need a room. When all floors are full, someone needs to build a new floor — that's where Karpenter and NodeClaims come in.

**Worked example:** Run `kubectl get nodes` and look at the output together:
```
NAME                          STATUS   ROLES    AGE   VERSION
ip-192-168-1-1.ec2.internal   Ready    <none>   2d    v1.28.3
```
Point out: this is one real machine currently in the cluster, ready to run Pods.

### What is a NodeClaim?
Karpenter is a Kubernetes add-on that automatically adds or removes nodes based on demand. When Karpenter decides a new node is needed, it doesn't create the node directly — it first creates a **NodeClaim**, which is like a purchase order or receipt: "I am requesting a node with these specs (instance type, zone, capacity type)." Kubernetes and the cloud provider then fulfill that claim by launching an actual machine, and once it joins the cluster, the NodeClaim links to that real Node.

**Worked example:** Run `kubectl get nodeclaims` together:
```
NAME            TYPE          ZONE         NODE                            READY   AGE
default-x7k2m   m5.xlarge     us-east-1a   ip-192-168-1-1.ec2.internal      True    3m
```
Walk through each column:
- `NAME` — the NodeClaim's own identifier (not the node's name)
- `TYPE` — the instance type Karpenter chose
- `NODE` — the actual Kubernetes Node this claim resolved to
- `READY` — whether the underlying node has joined and is usable

Then run `kubectl describe nodeclaim default-x7k2m` and point out the `Conditions` section, showing states like `Launched`, `Registered`, and `Initialized` — this is the lifecycle of a node being born.

---

## Differentiation

**For those who need more support:**
- Provide a printed/digital cheat sheet with the three commands (`get nodes`, `get nodeclaims`, `describe nodeclaim`) and one-line descriptions of each
- Use the apartment-building analogy repeatedly and let the learner draw the diagram themselves instead of just watching
- Reduce scope: focus only on `kubectl get nodeclaims` and reading the READY column, skipping `describe` output details if time-strapped

**For those ready for a challenge:**
- Introduce `kubectl get nodeclaims -o yaml` and have them identify the `spec.requirements` field (what constraints Karpenter used to pick the instance)
- Ask them to predict what would happen to the NodeClaim if the underlying node were deleted, then test it live if a sandbox cluster allows

---

## Formative Assessment (Check for Understanding)

**During session:**
- After the guided demo, ask: "In your own words, what's the difference between a Node and a NodeClaim?" — listen for the "actual machine vs. request/receipt" distinction
- Before independent practice, do a quick thumbs-up/thumbs-down: "Thumbs up if you feel ready to run these commands yourself"

**Exit ticket (last 5 minutes):**
"Using the terminal, run `kubectl describe nodeclaim` on any NodeClaim in the cluster and tell me: (1) what instance type was requested, and (2) whether it's currently Ready. Then explain what would trigger Karpenter to create a brand new NodeClaim."

---

## Common Misconceptions to Address

| Misconception | Correct understanding | How to address it |
|---|---|---|
| A NodeClaim *is* the node | A NodeClaim is a request/record object; the Node is the actual machine that fulfills it | Show both `kubectl get nodes` and `kubectl get nodeclaims` side by side and point out they have different names and different object counts when a node is still launching |
| NodeClaims must be created manually by the user | NodeClaims are automatically created and managed by Karpenter based on Pod scheduling pressure | Demonstrate (or describe) a Pod being stuck in `Pending`, then show Karpenter creating a NodeClaim in response, without any manual `kubectl create` |
| Deleting a NodeClaim is like deleting a Pod (low risk) | Deleting a NodeClaim triggers termination of the underlying cloud instance, which can disrupt running workloads | Explicitly state this and, if using a real cluster, avoid deleting NodeClaims during this session — mention it only as a warning |

---

## Quality Checks

- [x] Learning objectives use action verbs (Explain, Apply, Interpret)
- [x] Session has a clear hook that establishes relevance
- [x] Activities are varied (discussion, demo, hands-on, verbal explanation)
- [x] Formative assessment checks the actual learning objective
- [x] Differentiation is specified for both support and extension
- [x] Timing adds up to 60 minutes