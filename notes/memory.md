# Memory
Building the Hack computer's main memory unit (RAM).

### Sequential Logic
So far (project 1 & 2) all operations happened instantaneously, completely disregarding the time component (combinatorial logic).

We want to be able to re-use hardware components (not just one-time I/O operations) in order to:
* create loops (e.g. `for i in range(100)`)
* work with intermediate results (e.g. `sum = sum + i`)

**Notes**
* in reality, time is continuous -> break down into integer time units
* one integer time unit is equivalent to one cycle of an oscillating input signal (**pyhsical**)
* integer time unit needs to be just a tiny bit longer than how long it takes for the physical signal to stabilize
* build-up time portion of the interval is ignored and only the stabilized portion is taken into account
* within one integer time unit, operations happen **instantaneously**
    * ignoring physical signal's build-up time

- combinatorial: `out[t] = function(in[t])`
- sequential: `out[t] = function(in[t-1])`
    - can also be a **combination** of input at time `t-1` and `t`
- we now have **states**!

### Flip Flops
Gates that can (*physically*) flip between two states are called **Flip Flops**. 
As such, Flip Flops will remember either of bit 0/1 at the end of time `t-1` in order to use it in time `t`.

The two *states* are therefore:

* "remembering **0**"
* "remembering **1**"

**Resources** <sub>(watch in order)</sub>
* [[YouTube: ***Ben Eater***] SR Latch](https://www.youtube.com/watch?v=KM0DdEaY5sY&list=PLEJ4ZX3tdB692QvbCDnn6wrJGU0kTMY8P&index=2&ab_channel=BenEater)
* [[YouTube: ***Ben Eater***] D Latch](https://www.youtube.com/watch?v=peCh_859q7Q&list=PLEJ4ZX3tdB692QvbCDnn6wrJGU0kTMY8P&index=3&ab_channel=BenEater)
* [[YouTube: ***Ben Eater***] D Flip Flop](https://www.youtube.com/watch?v=YW-_GkUguMM&list=PLEJ4ZX3tdB692QvbCDnn6wrJGU0kTMY8P&index=4&ab_channel=BenEater)
* [[YouTube: ***Ben Eater***] JK Flip Flop](https://www.youtube.com/watch?v=F1OC5e7Tn_o&list=PLEJ4ZX3tdB692QvbCDnn6wrJGU0kTMY8P&index=5&ab_channel=BenEater)
* [[YouTube: ***Ben Eater***] Master-Slave JK Flip Flop](https://www.youtube.com/watch?v=rXHSB5w7CyE&list=PLEJ4ZX3tdB692QvbCDnn6wrJGU0kTMY8P&index=7&ab_channel=BenEater)
* [[YouTube: ***Ben Eater***] Astable Oscillator (*Clock*)](https://www.youtube.com/watch?v=kRlSFm519Bo&ab_channel=BenEater)

### RAM
Random Access Memory (RAM) is a chip that holds data *indefinitely* (that is, until the next load operation tells it to hold new data).

In contrast to sequential access (one after another), registers within RAM can be accessed arbitrarily, hence "random".

Each Register in the RAM structure holds exactly one 16-bit (in *this* implementation) binary number.

**Structure**
> **RAM** \
> (stores *K* * *N* bits of information)
>> *N* **Multi-bit Register** \
>> (each stores *K* bits of information)
>>> *K* **1-bit Register** \
>>> (each stores *1* bit of information)
>>>> Mux + D Flip Flop

---
### Project: Circuits
As implemented using HDL in [project 3](../projects/03/).

* [Bit](../diagrams/bit.png)
* [Register](../diagrams/register.png)
* [RAM8](../diagrams/ram8.png)
* *RAM64*, *RAM512*, *RAM4K* and *RAM16K* are trivial and similar to *RAM8* (Registers are replaced by higher order RAM chips in each iteration)
* [PC](../diagrams/pc.png)
