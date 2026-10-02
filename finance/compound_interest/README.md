# Compound Interest

## Mathematical model

A(t) = P(1+r)^t

The model is deliberately isolated from rendering. A renderer receives values
from this model; it does not calculate financial truth itself.

## First visual experiment

Compare:

- simple interest: P(1 + rt)
- compound interest: P(1 + r)^t

The first animation should show the same starting principal and the two growth
mechanisms diverging over time.

## Visual vocabulary

- particles for money
- recursive reinvestment
- exponential curve
- timeline
- accumulated area

## Implementation

The numerical model lives in:

engine/models/compound_interest.py
