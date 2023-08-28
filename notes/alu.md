# Boolean Arithmetic and the ALU
As implemented using HDL in [project 2](../projects/02/).

* [HalfAdder](../diagrams/halfadder.png) (**Note**: Two half adders are required to build one full adder - hence the name)
* [FullAdder](../diagrams/fulladder.png)
* [Add16](../diagrams/add16.png)
    * uses two XOR gates to compute the msb output
    * this reduces the number of total gates used compared to a naive, HalfAdder + 15 FullAdder implementation
    * **Note**: 2's complement is a **convention** and requires implementation; the Adder has **no way** of "knowing" whether it performs *addition* or *subtraction*
* [ALU](../diagrams/alu.png)
    * uses two *Mux4Way16* to handle input transformations
    * output is routed to **out**, **ng** & **zr** from the final *Mux16*
        * output's msb suffices as an indicator for negative/positive output values
        * output's lowest & highest 8 bits are routed into separate 8-way OR gates to check for 0 output

**Resources**
* [[YouTube: ***Khan Academy***] Binary Addition](https://www.youtube.com/watch?v=RgklPQ8rbkg&ab_channel=KhanAcademy)
* [[YouTube: ***Computerphile***] Two's Complement](https://www.youtube.com/watch?v=lKTsv6iVxV4&ab_channel=Computerphile)