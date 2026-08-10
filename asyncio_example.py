# ==========================================
# #example without async
# ==========================================

# import time
# print("CODE 1")

# print("="*30,"\n")
# def download_file(file_no):
#     print(f"file is downloading={file_no}")
#     time.sleep(1)
#     print(f"file downloaded={file_no}")
    
    
# start=time.time()
# download_file(1)
# download_file(2)
# download_file(3)

# end=time.time()

# print(f"time taken= {end-start}")

# ==========================================
# #example with asyncio   
# ==========================================

# import time
# import asyncio

# print("CODE 2")
# print("="*30,"\n")

# async def downloading_file(file_no):
#     print("file is downloading=",file_no)
#     asyncio.sleep(1)
#     print("file is downloaded completely=", file_no)
    
# async def main():
#     start=time.time()
#     task1=asyncio.create_task(downloading_file(1))
#     task2=asyncio.create_task(downloading_file(2))
#     task3=asyncio.create_task(downloading_file(3))
    
#     await task1
#     await task2
#     await task3
    
#     end=time.time()
    
#     print("time_taken",end-start)


# asyncio.run(main())

#asyncio.sleep help the program to run further things while, waiting for some process
# diffrence between asyncio.sleep and time.sleep is that, time.sleep hold the wole program and wait 
# till the time completes, where as asyncio.sleep hold that specific task and run other things in the mean time 

# ==========================================
# asyncio with gather function
# ==========================================

# import asyncio
# import time

# print("CODE 3")
# print("="*30,"\n")

# async def file_downloading(file_no):
#     print("file is downlaoding=",file_no)
#     await asyncio.sleep(1)
#     print("file is downloaded completely",file_no)
    
    
# async def main():
#     start=time.time()
#     await asyncio.gather(
#         file_downloading(1),
#         file_downloading(2),
#         file_downloading(3)
#     )
    
#     end=time.time()
    
#     print("time taken=",end-start)
    
# asyncio.run(main())


# =========================================
# returning data from coroutine
# ==========================================

# import time,asyncio

# print("CODE 4")

# async def fetch_data(data):
#     print("fetching the data no.=",data)
#     await asyncio.sleep(1)
#     return(f"data={data}")
    
# async def main():
#     start=time.time()
#     results=await asyncio.gather(
#         fetch_data(1),
#         fetch_data(2),
#         fetch_data(3)
#     )
#     print(results)
#     end=time.time()
    
#     print("time taken=",end-start)
    
# asyncio.run(main())

# ==========================================
# working in couroutine with the blocking task
# ==========================================

# import asyncio, time

# print("CODE 5")
# def blocking_task():
#     print("blocking task is in the process....")
#     time.sleep(1)
#     print("blocking task completed.")
    
# async def non_blocking_task():
#     print("non blocking task running......")
#     await asyncio.sleep(1)
#     print("non blocking task completed.")
    
# async def main():
#     start=time.time()
#     print("starting coroutine")
#     loop=asyncio.get_running_loop()
    
#     await loop.run_in_executor(None,blocking_task)
#     await asyncio.create_task(non_blocking_task())
    
#     print("main coroutine start after blocking task")
#     end=time.time()
    
#     print("\n\n\ntime taken",end-start)

# asyncio.run(main())


# asyncio.run(main())

# ==========================================
# working in couroutine with the blocking task
# ==========================================

# import asyncio, time

# print("CODE 5")
# async def blocking_task():
#     print("blocking task is in the process....")
#     time.sleep(1)
#     print("blocking task completed.")
    
# async def non_blocking_task():
#     print("non blocking tas running......")
#     await asyncio.sleep(1)
#     print("non blocking task completed.")
    
# async def main():
#     start=time.time()
#     print("starting coroutine")
#     loop=asyncio.get_running_loop()
    
#     await loop.run_in_executor(None,blocking_task)
#     await asyncio.create_task(non_blocking_task())
    
#     print("main coroutine start after blocking task")
#     end=time.time()
    
#     print("\n\n\ntime taken",end-start)

# asyncio.run(main())

# ==========================================
# for loop in asyncio 
# ==========================================


import asyncio, time

print("CODE 6")

async def countdown():
    for i in range(3):
        await asyncio.sleep(1)
        yield i

async def main():
    start=time.time()
    async for value in countdown():
        print("count",value)
    end=time.time()
    print("time taken",end-start)
    
asyncio.run(main())



