# Decompiler Usage Guide

---

## **Table of Contents**
- **Syntax Overview**
  - Commands
    - Org Directive
    - Bracketed skip section
    - Note Directive
  - Program Structure Overvie
- **Examples**
  - Example 1: Simple Program
  - Example 2: Using skip command
  - Example 3: Using note command

---

## **Syntax Overview**

### **Commands**

- **Org Directive**
  - Set code mapping address:  
    `ADDR <expr>:`
- **Bracketed skip section**
  - Ignore extra bytes during decompiler:
    `[<hex_bytes>]`
- **Note Directive**
  - Attach comment or metadata:
    `(<comment>)`

### **Program Structure Overview**
```
ADDR <address>:
<your code>
...
```

---

## **Examples**

### **Example 1: Simple Program**
input:
```text
ADDR E9E0:
34 7B 31 30 30 30 30 30 C8 3D 32 30 7E 94 30 30
```

output:
```text
org 0xE9E0:

xr0 = hex 30 30 30 30
printline
render.ddd4
```

### **Example 2: Using skip command**
input:
```text
ADDR E9E0:
34 7B 31 30 30 30 30 30 [C8 3D 32 30] 7E 94 30 30
```
output:
```text
org 0xE9E0:

xr0 = hex 30 30 30 30
hex c8 3d 32 30
render.ddd4
```

### **Example 3: Using note command**
input:
```text
ADDR E9E0:
34 7B 31 30 30 30 30 30 C8 3D 32 30 7E 94 30 30 (above is the print and rendering processing)
```

output:
```text
org 0xE9E0:

xr0 = hex 30 30 30 30
printline
render.ddd4
note "above is the print and rendering processing"
```

---

###### Written by luongvantam
