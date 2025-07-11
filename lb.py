import json

def main():
	with open("data.json") as file:
		data = json.load(file)
	data.sort(key=lambda x: x[2], reverse=True)
	for i in range(0, len(data)):
		print(f"top {i+1}: {data[i][1]} {data[i][2]}")

if __name__ == "__main__":
	main()