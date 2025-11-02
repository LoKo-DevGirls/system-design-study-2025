# Ticket booking system : ticket-master
- 19th Oct ~ 26th Oct

# Summary
As a first-pass [conceptual sketch](https://github.com/LoKo-DevGirls/system-design-study-2025/pull/2#issuecomment-3448305665) for discussion, we created a flow chart and attached it to the [PR](https://github.com/LoKo-DevGirls/system-design-study-2025/pull/2).

We identified several foundational components of a modern, service-oriented system. During the session, we demonstrated a good understanding of the need to centralise and manage ingress traffic.

Following the system requirements we set out, the high-level design derived was for a system having a gateway that directs requests to a central processing unit (API), which in turn communicates with distinct, domain-orientated services such as search, booking, and payment.

Furthermore, we included a DB component to acknowledge the fundamental requirement for a persistent data store.