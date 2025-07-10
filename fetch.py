import os
import json
import requests as rq
import tqdm
from dotenv import load_dotenv

FIELDS=["tag", "name"]

def getClans():
	load_dotenv()
	return json.loads(os.getenv('CLANS'))

def getToken():
	load_dotenv()
	return os.getenv("KEY")

def getClanMembers(headers, clan):
	r = rq.get(headers=headers, url=f"https://api.clashroyale.com/v1/clans/%23{clan}/members")
	if r.status_code != 200:
		return
	return r.json()

def getFullMemberList(headers, clans):
	members = []
	data = []
	for clan in clans:
		data += getClanMembers(headers, clan)['items']
	for member in data:
		members.append([member["tag"], member["name"]])
	return members

def	getMergeTacticRanking(headers, id):
	r = rq.get(headers=headers, url=f"https://api.clashroyale.com/v1/players/%23{id[1:]}")
	if r.status_code != 200:
		print(r.status_code)
		print(r.reason)
		return
	return r.json()

def addMergeTacticRanking(headers, members):
	for i in tqdm.tqdm(range(0, len(members))):
		rating = getMergeTacticRanking(headers, members[i][0])
		if (rating and 'progress' in rating and 'AutoChess' in rating['progress'] and 'trophies' in rating['progress']['AutoChess']):
			members[i].append(rating['progress']['AutoChess']['trophies'])
		else:
			members[i].append(0)
	with open("data.json", "w") as file:
		json.dump(members, file, indent=4)

def main():
	token = getToken()
	clans = getClans()
	if not token:
		print("Missing token in .env")
		return
	if not clans:
		print("Missing clans in .env")
		return
	headers = {"Authorization": f"Bearer {token}"}
	members = getFullMemberList(headers, clans)
	addMergeTacticRanking(headers, members)

if __name__ == "__main__":
	main()
