# Half and Half
Crypto

## Challenge 

Mm, coffee. Best served with half and half!

Author: defund

[half_and_half.py](half_and_half.py)

## Solution

As seen in the code

```python
half = len(flag)//2
milk = flag[:half]
cream = flag[half:]

assert xor(milk, cream) == '\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"'
```
Working operation:

- The flag is split into 2 halves.
- After which, the halves are XOR-ed together
- Resultant string is 12 chars long.

We know from the flag format that:

- `milk` starts with `actf{`
- `cream` ends with `}`

We can recover 6 of the 12 chars.

Python shell

	def xor(x, y):
		o = ''
		for i in range(len(x)):
			o += chr(ord(x[i])^ord(y[i]))
		return o

	encoded = '\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"'

	>>> print(xor('actf{', encoded))
	taste

	>>> print(xor('\x00' * 11 + '}', encoded)[-1])
	_

Fill in the progress

	actf{      _taste      }
	123456789ABC123456789ABC

---

From the challenge, we have the hint of coffee

	>>> print(xor('actf{coffee', encoded))
	tastes_good

Fill in the progress again

	actf{coffee_tastes_good}
	123456789ABC123456789ABC

## Flag

	actf{coffee_tastes_good}
