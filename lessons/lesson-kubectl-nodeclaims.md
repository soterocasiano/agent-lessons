# Lesson Plan: kubectl NodeClaims

**Subject:** Kubernetes / Karpenter (Cloud-Native Infrastructure) | **Audience:** General audience, no prior experience assumed
**Duration:** 60 minutes | **Setting:** 1-on-1 | **Group size:** 1

---

## Learning Objectives

By the end of this session, participants will be able to:
1. Explain what a NodeClaim is and how it relates to Karpenter and Kubernetes nodes.
2. Use `kubectl` commands to list, inspect, and describe NodeClaims.
3. Interpret a NodeClaim's status fields to determine whether a node is healthy, provisioning, or has an issue.
4. Apply this knowledge to troubleshoot a basic node-provisioning problem using NodeClaim information.

**Key vocabulary:** NodeClaim, Karpenter, Node, Provisioning, Custom Resource Definition (CRD), Status Conditions

---

## Materials and Preparation

- [ ] A terminal with `kubectl` configured against a cluster running Karpenter (test/sandbox cluster preferred)
- [ ] At least one NodeClaim resource existing in the cluster (create one via a test workload if needed)
- [ ] Screen-share enabled for live command demonstration
- [ ] Optional: printed or shared cheat-sheet of `kubectl get/describe` command syntax
- [ ] Room setup: Side-by-side seating or shared screen, one shared terminal

---

## Lesson Structure

| Time | Phase | Activity | Format |
|---|---|---|---|
| [00:00] | Hook / Opener | Ask: "When you deploy a workload and Kubernetes needs a new server to run it — how does it actually get one?" Briefly show a live cluster scaling up a node in real time. | Discussion |
| [00:05] | Prior knowledge | Quick check: "Have you heard of Kubernetes Nodes? Pods? Autoscaling?" Calibrate depth based on answers — no assumption of prior knowledge. | Q&A |
| [00:15] | Instruction | Explain what a NodeClaim is: a Karpenter custom resource representing a *request* for a node, tracking its lifecycle from request to ready. Contrast with a plain Kubernetes Node object. | Explanation + Diagram |
| [00:30] | Guided practice | Together, run `kubectl get nodeclaims`, then `kubectl describe nodeclaim <name>`. Walk through the output field by field (status, conditions, resources, nodeClass reference). | Live terminal walkthrough |
| [00:45] | Independent practice | Participant runs the commands themselves on a different NodeClaim (or triggers a new one by scaling a deployment) and reports back what they observe. | Hands-on task |
| [00:53] | Check for understanding | Ask participant to identify, from a `describe` output, whether the NodeClaim is Ready, still Launching, or has an error condition. | Q&A / Live output review |
| [00:57] | Closure | Summarize NodeClaim lifecycle (Pending → Launched → Registered → Ready) and how it connects Pods to Nodes. Preview next topic: NodePools/NodeClasses. | Discussion |

---

## Key Explanations and Worked Examples

### What is a NodeClaim?
A NodeClaim is a Kubernetes custom resource (CRD) created by Karpenter to represent a **request for compute capacity** — essentially "I need a node with these specs." It exists *before* the actual cloud instance and Kubernetes Node object are created, and it tracks the full lifecycle until the node is ready to run workloads. Think of it like an order receipt: the NodeClaim is the paper trail proving a node was requested, what was asked for, and whether it arrived successfully.

**Worked example:**
```
kubectl get nodeclaims
NAME            TYPE          ZONE         NODE                READY   AGE
default-abc12   m5.large      us-east-1a   ip-10-0-1-23...      True    5m
```
This tells us Karpenter requested an `m5.large` instance, it landed in `us-east-1a`, it's linked to a specific Node object, and it's `Ready` — meaning it can now schedule Pods.

### Reading NodeClaim Status with `describe`
Running `kubectl describe nodeclaim <name>` reveals **Status.Conditions**, a list of true/false checks like `Launched`, `Registered`, `Initialized`, and `Ready`. These conditions fire in sequence as the node moves from "just requested" to "fully operational."

**Worked example:**
```
Status:
  Conditions:
    Type:    Launched      Status: True
    Type:    Registered    Status: True
    Type:    Initialized   Status: False   Reason: NodeNotReady
    Type:    Ready         Status: False
```
This tells us the cloud instance launched and joined the cluster, but it isn't fully initialized yet — useful for spotting exactly where a stuck node is failing.

---

## Differentiation

**For those who need more support:**
- Provide a simple analogy sheet: "NodeClaim = restaurant order ticket, Node = the meal that arrives"
- Pre-highlight the 2–3 most important fields in a sample `describe` output before asking them to interpret it themselves
- Allow them to read output aloud with guided prompts ("What does the Ready field say?") instead of open-ended interpretation

**For those ready for a challenge:**
- Ask them to correlate a NodeClaim with its underlying cloud instance ID and Kubernetes Node object using `kubectl get node -o wide`
- Introduce `kubectl get nodeclaim -o yaml` to explore the full spec (resource requests, taints, NodeClass reference) unprompted

---

## Formative Assessment (Check for Understanding)

**During session:**
- Ask participant to narrate what a live `describe` output means, field by field, before I confirm/correct
- Think-aloud check: "If Ready is False, what would you check next?"

**Exit ticket (last 5 minutes):**
"Here's a `kubectl describe nodeclaim` output on screen — is this NodeClaim healthy? If not, what's the first condition that failed, and what would that suggest is going wrong?"

---

## Common Misconceptions to Address

| Misconception | Correct understanding | How to address it |
|---|---|---|
| A NodeClaim *is* the Node | A NodeClaim is a request/tracking object; the Node is the actual Kubernetes object representing the running machine once joined | Show both objects side-by-side (`kubectl get nodeclaims` vs `kubectl get nodes`) and point out the linkage field |
| NodeClaims are manually created by users | NodeClaims are automatically created by Karpenter in response to unschedulable Pods | Demonstrate a Pod triggering a new NodeClaim live, or explain the trigger chain verbally if live demo isn't possible |
| A `Ready: False` NodeClaim means something is broken | It may simply be mid-provisioning (normal transient state) | Point out the sequential conditions (Launched → Registered → Initialized → Ready) and explain timing expectations |

---

## Quality Checks

- [x] Learning objectives use action verbs (explain, use, interpret, apply)
- [x] Session has a clear hook that establishes relevance (live scaling demo)
- [x] Activities are varied (discussion, explanation, live terminal, hands-on, Q&A)
- [x] Formative assessment checks the actual learning objective (interpreting NodeClaim status)
- [x] Differentiation specified for both support and extension
- [x] Timing adds up to 60 minutes (00:00–00:57, closing by 01:00)