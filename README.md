# Minecraft-Bedrock-XP

# A Python script to read and modify the experience level in Minecraft Bedrock Edition. This project demonstrates how to locate dynamic memory addresses, create pointer chains, and automate XP manipulation using Cheat Engine and Python.
# This also works on realm servers.

In this tutorial, I will be showing you how I was able to find and change my experience level using Cheat Engine.

The first step was to find the dynamic memory address for the experience level, as well as the data type that is used.

To do this, I first had to assume that the experience level would be a float, I came accross this conclusion because a float allows for fractional values.

With that, I was ready to do my first memory scan, to do this I had to first give my local player experience. After doing this, I did a memory scan for the value of my experience level, using a float as the data type.

As such:

![image](https://github.com/user-attachments/assets/e2c40a94-9c68-4f9c-9577-e7bceff39c8f)

After doing this, you notice a long list of values that have the same value as my experience level, however, not all of these are correlating to that value.

So, to narrow down my search, I changed my xp level again. After doing this, my search was narrowed down to only 2 memory addresses.

One of which represented the value of my experience level, and the other represented a similar function that only wrote the numbers to the screen of my XP bar.

The only one you need to worry about, is the one that actually changes your experience level. You can do this by double clicking both values, and putting them in your memory address list.

Once you've done this, you need to singularly change both values, don't do it at the same time because you're trying to isolate only one of these memory addesses to find the one directly correlating to the experience level.

Once you've done that, you should have a dynamic memory address that correlates to your experience level where you can change & edit this level.

![image](https://github.com/user-attachments/assets/531c8375-6a95-4861-a320-31fecfd241d3)

At this point, you have hacked your experience level. You can choose to do this every time, or you can find a static memory addess so you don't have to manually find the memory address correlating to the experience level each time.

You have to do this, because ```the dynamic memory address changes every time you restart or leave the game```, that's why it is dynamic.

If you want to write a python script using only the dynamic memory address, you can do so by finding the registers that directly corelate to the dynamic memory address. This will show you the offsets & instructions needed to do so.

In order to do this, you can right click on your dynamic memory address, and click ```"find out what accesses this address."``` Here you will see the memory instructions.

![image](https://github.com/user-attachments/assets/45129846-5319-4dd7-bed6-5bc1054964e4)

You can notice that ```rsi and 00000084```, are commonly written in these instructions.

So we can assume that ```rsi + 0x84 = dynamic memory address```. Now we need to find what the value of rsi is.

To do so is simple, we have to click on one of the instructions containing ```rsi + 0x84```

![image](https://github.com/user-attachments/assets/7b32e1f8-8a26-44a4-9dfa-b1f7fae53834)

Here, we can see at the bottom ```"RSI=000001347C195C28"``` This is what we're looking for.

Now we know 

```
0x1347C195C28 + 0x84 = xp level.
```

It's important to note that all memory addresses here are still dynamic, other than 0x84, which is a common instruction that is given with your experience level.

So now that we have this information, let's go on ahead and test this hypothesis in a python script relying on this dynamic information, keep in mind this part is not static, so you will have to find the value for RSI every time you restart or leave the game.

```
import pymem
import struct

pm = pymem.Pymem('Minecraft.Windows.exe')

rsi_address = 0x1347C195C28
offset_xp = 0x84
xp_address = rsi_address + offset_xp

current_xp_value = pm.read_float(xp_address)
print(f"Current XP value: {current_xp_value}")
```

Doing this, you should get an output that successfully reads your XP value.


Now that I have explained this, let's get into the more complex area of finding a pointer that brings us to our experience level.


So, to further this process, you can find a pointer, which is a base address + memory address + instructions, or offsets.

- A pointer is a memory address that stores the location of another memory address.

To do this, we want to go back to our dynamic memory address for our experience level that we found first thing.

It's not necessary, but I recommend that you first change the description for this dynamic memory address to something easier to understand, such as xp_1.

![image](https://github.com/user-attachments/assets/834d849b-0229-4f54-ae5d-9addb2be6b4c)


Aftet you've done that, you want to right click this memory address and click ```generate pointer map,``` from here you want to save this file as something simple to not get things confused as well, such as xp_1

After you've done this, you want to leave and rejoin the game, then repeat the process of finding the dynamic memory address again. 

Do this by following the first steps we discussed:

change your exp value, search for it, change it again, search for it again, change the value of exp to verify memory address.

Now that you have successfully found the dynamic mem address for exp again, you want to give this another easy description, such as xp_2.

![image](https://github.com/user-attachments/assets/620fc487-8b3f-4844-96e7-1ede1a26d94f)

Follow the same steps as before and generate another pointer map, call this file xp_2.


After you've done this, right click on the mem address for xp_2 and click ```pointer scan for this address,``` 

From here a new window should pop up, directly underneath the memory address which should automatically be highlighted, select ```compare resutls with over saved pointermap(s)```

![image](https://github.com/user-attachments/assets/5003d319-45b8-4095-a27b-07dade25d28e)

From here, you want to select xp_1, and make sure the address for this in the drop down menu also says xp_1 for the description

![image](https://github.com/user-attachments/assets/d85c96ae-d1fb-4c83-8879-bef9aa9bd15d)

Give this a moment to load, and then you should find a bunch of different pointers correlating to your experience value, however, not all of these are stable.

To find the stable pointers that always point to your xp value, you want to leave this screen open and then leave and rejoin Mincraft again, you will see some of the values of these pointers change, and some of them will stay your xp level.

You want to do this 2-3 times before deciding which pointer to go with, after you've done that, double click one of the pointers, this will automatically add it to your memory list. 

It should look like this, doesn't have to be exact:

![image](https://github.com/user-attachments/assets/1331d16c-41b4-4049-8957-73b23b7dd962)

To verify it changes your xp level, you can change the value of the pointer and see if your xp value changes, if it does, you were successful.

Now we need to make a python script using the pointer scan information.

Double click on the pointer you have found and look at it's information..

![image](https://github.com/user-attachments/assets/b5bf45ad-33a2-449b-9332-00b70805f943)

Here, we can see a lot of different values that make this look really complex and confusing. But I promise you, it's not. Stick with me here.

Here can see ```Minecraft.Windows.exe"+06A4D1E8``` at the bottom of this menu, this is the base address of the pointer chain.

It combines the base address of the ```Minecraft.Windows.exe``` module with an offset ```0x06A4D1E8```.

Those instructions that you see above that, ```EE0, E0, E0, 300, 170, 8, 8, 8, 9C``` are step-by-step offsets applied to resolve the final memory address.

Here, this works by starting at the base address, calculating it as ```base_address_of_Minecraft.Windows.exe + 0x06A4D1E8.```
This is then dereferenced (read the memory at this location), and add EE0 to get the next address.
And then this process is continued with the other offsets, or instructions; repeat for each offset ```E0, E0, 300, etc..```
The final offset ```9C``` gives the exact memory address where the experience level value, ```stored as a float,``` is located.

Now that we understand this, let's use it in a python script to always have a way to find our experience level without having to use cheat engine for a dynamic memory address each time.

```
import pymem
import pymem.process

pm = pymem.Pymem("Minecraft.Windows.exe")

base_address = pymem.process.module_from_name(pm.process_handle, "Minecraft.Windows.exe").lpBaseOfDll

base_pointer_offset = 0x06A4D1E8

offsets = [0xEE0, 0xE0, 0xE0, 0x300, 0x170, 0x8, 0x8, 0x8, 0x9C]

current_address = base_address + base_pointer_offset
for offset in offsets:
    current_address = pm.read_longlong(current_address) + offset

current_xp_value = pm.read_float(current_address)
print(f"Current XP value: {current_xp_value}")
```

 
