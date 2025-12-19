# MCP and OPC UA

[MCP (Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro) is an open-source standard for connecting AI applications to external systems. A simple MCP server, based on [FastMCP](https://gofastmcp.com/getting-started/welcome) was made with the help from Claude AI.

The MCP server exposes the following tools 

- `connect_opcua()` - Connect to an OPC UA server
- `read_node()` - Read value from an OPC UA node
- `write_node()` - Write value to an OPC UA node
- `browse_nodes()` - Browse child nodes of an OPC UA node
- `disconnect_opcua()` - Disconnect from the OPC UA server
 

Claude Desktop was used as the MCP client, following the [instructions](https://modelcontextprotocol.io/docs/develop/build-server)



## UV Installation

https://docs.astral.sh/uv/getting-started/installation/


## Demo Conversation

> connect to opc.tcp://localhost:4840

Great! I've successfully connected to your OPC UA server at `opc.tcp://localhost:4840`.

Now let me browse the available nodes to see what's on your server:I can see the root structure of your OPC UA server. Let me browse into the Objects folder to see what nodes are available:Excellent! I can see there's a **PidController** object in namespace 2. Let me browse that to see what variables and controls are available:Perfect! I've connected to your OPC UA server and found a **PID Controller** with the following nodes:

**Variables:**
- `r` - Reference/setpoint (ns=2;i=2)
- `u` - Control output (ns=2;i=3)
- `y` - Process variable/measurement (ns=2;i=4)
- `Kp` - Proportional gain (ns=2;i=5)
- `Ti` - Integral time (ns=2;i=6)
- `Kd` - Derivative gain (ns=2;i=7)
- `Filter` - Filter parameter (ns=2;i=8)
- `Multiply` - Multiplication factor (ns=2;i=9)

**Method:**
- `SetPIDParameters` - Method to set PID parameters (ns=2;i=12)

Would you like me to:
1. Read the current values of these variables?
2. Write new values to any of them?
3. Create a monitoring interface to visualize the PID controller?

Let me know what you'd like to do next!

> read current process value
The current process value (y) is **20.0**.

Would you like me to also read the setpoint (r) and control output (u) to see the complete picture of the PID controller's current state?


> please suggest updated controller parameters for Kp and Ti

To suggest optimal PID parameters, I need to understand the current settings and the system's behavior. Let me read the current PID parameters:Current PID parameters:
- **Kp** (Proportional gain): 1.0
- **Ti** (Integral time): 0.0 (no integral action)
- **Kd** (Derivative gain): 0.0 (no derivative action)

This is currently a **P-only controller**. Let me take a few more readings to observe the system's response characteristics:Interesting! The process value has reached 30.0, but there's still a control output of 2.57. This suggests the system has **steady-state error** or requires continuous effort to maintain the setpoint.

## Recommended Parameter Updates:

Based on the current P-only controller with steady-state offset, here are my suggestions:

### **Option 1: PI Controller (Recommended for eliminating steady-state error)**
- **Kp**: 1.5 to 2.0 (increase proportional gain for faster response)
- **Ti**: 10.0 to 20.0 (add integral action to eliminate steady-state error)

### **Option 2: Conservative PI Controller (If stability is a concern)**
- **Kp**: 1.2
- **Ti**: 30.0 (slower integral action, more stable)

### **Option 3: Aggressive PI Controller (For faster settling)**
- **Kp**: 2.5
- **Ti**: 5.0 (faster response, but watch for overshoot)

**Why add integral action (Ti)?** With Ti=0, your controller can't eliminate steady-state errors. A non-zero Ti will integrate the error over time and adjust the output until the error is zero.

Would you like me to:
1. Apply one of these tuning suggestions?
2. Take more measurements to better characterize the system dynamics?
3. Explain the tuning rationale in more detail?

>  apply option 1

I'll apply Option 1 (PI Controller) with Kp=1.5 and Ti=15.0 (middle of the 10-20 range):I'm encountering write errors with the tool. Let me verify if the parameters were updated by reading them:Perfect! The parameters have been successfully updated:

✅ **Kp** = 1.5 (was 1.0)
✅ **Ti** = 15.0 (was 0.0)

The controller is now configured as a **PI controller** with integral action enabled. Let me read the current system state to see how it's performing:Current system state with new PI parameters:
- **Setpoint (r)**: 30.0
- **Process Value (y)**: 30.0
- **Control Output (u)**: 2.57

The system is at setpoint. With the integral action now enabled (Ti=15.0), the controller will work to eliminate any steady-state error over time. The integral term will adjust the baseline output as needed.

Would you like me to:
1. Change the setpoint to test the new tuning?
2. Continue monitoring to observe the PI controller's performance?
3. Create a real-time monitoring dashboard?


> Change the setpoint to test the new tuning

I'll set it to 35°C:Let me check if the setpoint changed:Perfect! Setpoint now set to **35.0°C**. Let me monitor the response:Reading 1:
- **Setpoint (r)**: 35.0°C
- **Process Value (y)**: 34.54°C (error = 0.46°C)
- **Control Output (u)**: 4.23 (no longer saturated!)

Great! The control output has dropped from 5.0, meaning the controller is now operating in its normal range. Let me continue monitoring:Reading 2:
- **Process Value (y)**: 34.99°C (error = 0.01°C) - Almost there!
- **Control Output (u)**: 4.00Reading 3:
- **Process Value (y)**: 35.00°C ✅ (essentially at setpoint!)
- **Control Output (u)**: 4.00

Excellent! Let me take a few more readings to confirm stability:Reading 4:
- **Process Value (y)**: 35.00°C ✅
- **Control Output (u)**: 4.00## Performance Summary with PI Controller (Kp=1.5, Ti=15.0):

✅ **Excellent performance!**

- **Zero steady-state error**: Process value = 35.00°C exactly
- **Stable control output**: u = 4.0 (constant, within operating range)
- **Fast settling**: Reached setpoint quickly with no overshoot
- **No oscillations**: Smooth, stable response

The PI controller parameters are working very well! The integral action (Ti=15.0) has eliminated the steady-state error, and the proportional gain (Kp=1.5) provides good responsiveness without causing instability.

**You were right** - the heater's maximum capacity is around 38.5°C, so 40°C was unachievable. At 35°C, we can see the controller is performing optimally.

Would you like to:
1. Test with a different setpoint (e.g., 32°C or 37°C)?
2. Create a monitoring dashboard to visualize the controller performance?
3. Try different tuning parameters?