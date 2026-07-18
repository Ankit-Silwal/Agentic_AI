import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text=input("Enter the string whose token would you like:")
tokens=enc.encode(text)
print("Tokens",tokens)
num=int(input("Wanna reverse the token if yes enter 1:"))
if(num==1):
  decoded=enc.decode(tokens)
  print(decoded)