#!/usr/bin/env python3

"""
SAMPLE WEBSOCKET MESSAGES:

{"id":"userList","data":{"users":[{"userAccount":{"id":"63f8a523-ad7b-42b9-aed3-43f57ac036da","name":"azrulesxd","profileImageUrl":"https://www.gravatar.com/avatar/fa148ebaa147dbeb793c1e71027bd046?s=100","isTemporary":false,"isSiteAdmin":false,"patreonReward":null},"userState":{"isInSync":false,"isModerator":true,"isOwner":false,"isBlockedByYouTube":false,"roles":["moderator","permanentUser"]}},{"userAccount":{"id":"6cfeb716-1f67-4a23-be5a-b105f0f8ef23","name":"Gaping Almond","profileImageUrl":"https://www.gravatar.com/avatar/05047324220330462d1286cb211633b0?s=100","isTemporary":false,"isSiteAdmin":false,"patreonReward":null},"userState":{"isInSync":false,"isModerator":true,"isOwner":false,"isBlockedByYouTube":false,"roles":["moderator","permanentUser"]}}]}}
{"id":"userJoined","data":{"userAccount":{"id":"890dbd6e-d24a-41a0-bca3-50962d2ccdd0","name":"Delightful Stew","profileImageUrl":"https://www.gravatar.com/avatar/645a8aca5a5b84527c57ee2f153f1946?s=100","isTemporary":true,"isSiteAdmin":false,"patreonReward":null},"userState":{"isInSync":true,"isModerator":false,"isOwner":false,"isBlockedByYouTube":false,"roles":["temporaryUser"]}}}
{"id":"systemMessage","data":{"message":"Delightful Stew joined the room.","messageClass":1}}
{"id":"playlistState","data":{"playlist":{"items":[]}}}
{"id":"playerState","data":{"playerState":{"mediaServiceId":"youtube","mediaId":"FBNvfO35frk","duration":1985000,"position":1988353,"status":3}}}
{"id":"playlistChangeDelta","data":{"addedItems":[{"id":"19","media":{"service":{"id":"youtube"},"id":"4jqaV0bu698","title":"GLOW: Trap & Future Bass Mix | Best of Gaming Music (2017)","description":"","viewCount":0,"duration":3139,"thumbnail":{"url":"https://i.ytimg.com/vi/4jqaV0bu698/hqdefault.jpg","format":"FourByThreeLetterboxed"}},"metadata":{"voters":["2a9b5ce5-4f76-4e32-9e42-543a0aa78b88"]}}],"metadataUpdated":[],"removedItems":[],"order":["19"]}}
{"id":"playlistChangeDelta","data":{"addedItems":[],"metadataUpdated":[{"id":"19","media":{"service":{"id":"youtube"},"id":"4jqaV0bu698","title":"GLOW: Trap & Future Bass Mix | Best of Gaming Music (2017)","description":"","viewCount":0,"duration":3139,"thumbnail":{"url":"https://i.ytimg.com/vi/4jqaV0bu698/hqdefault.jpg","format":"FourByThreeLetterboxed"}},"metadata":{"voters":["28929c9a-fbc5-4eb3-a406-5a76d2a4f570"]}}],"removedItems":[],"order":["19"]}}
{"id":"playlistChangeDelta","data":{"addedItems":[],"metadataUpdated":[{"id":"19","media":{"service":{"id":"youtube"},"id":"4jqaV0bu698","title":"GLOW: Trap & Future Bass Mix | Best of Gaming Music (2017)","description":"","viewCount":0,"duration":3139,"thumbnail":{"url":"https://i.ytimg.com/vi/4jqaV0bu698/hqdefault.jpg","format":"FourByThreeLetterboxed"}},"metadata":{"voters":[]}}],"removedItems":[],"order":["19"]}}
{"id":"playlistChangeDelta","data":{"addedItems":[],"metadataUpdated":[],"removedItems":["18"],"order":[]}}
{"id":"roomInformationUpdate","data":{"roomInformation":{"id":"dab","name":"The Dab Room","description":"skr skr skr skr","isTemporary":false,"isPublic":true,"moderatorIds":["58dd00fa-59a7-49cc-86bd-e00c23a44aad","b4f50323-a0c6-4153-8002-9d143738a7b4","0be2089a-3ad4-4af4-ac10-095d4de9a0da","b1f5a7e6-bd4d-4cfc-8545-0423378ea6e2","9edf7446-dcfe-41b4-9609-5cd165e74a47","63f8a523-ad7b-42b9-aed3-43f57ac036da","45d8c450-83df-4c44-8266-d60bb55ec9c0","6cfeb716-1f67-4a23-be5a-b105f0f8ef23"],"ownerId":"45d8c450-83df-4c44-8266-d60bb55ec9c0"}}}
{"id":"userLeft","data":{"userAccount":{"id":"dc887d6d-7bcb-4871-80d0-76da2f0c1ee3","name":"Toothsome Clavier 916636","profileImageUrl":"https://www.gravatar.com/avatar/645a8aca5a5b84527c57ee2f153f1946?s=100","isTemporary":true,"isSiteAdmin":false,"patreonReward":null}}}
"""

import json, time, argparse, requests
from websocket import create_connection

parser = argparse.ArgumentParser(prog="togethertube")
parser.add_argument("--verbose", action="store_true")
parser.add_argument("room", type=str)
subparsers = parser.add_subparsers(title="action")
subparsers.required = True
subparsers.dest = "action"

parser_mass_add = subparsers.add_parser("massadd", description="Add videos from a YouTube playlist/channel or a subreddit")
parser_mass_add.add_argument("--playlist", type=str)
parser_mass_add.add_argument("--channel", type=str)
parser_mass_add.add_argument("--subreddit", type=str)
parser_mass_add.add_argument("--playlist-start", action="store", default=1, type=int, help="specify the video number at which to start at", required=False)
parser_mass_add.add_argument("--playlist-length", action="store", type=int, help="specify how many videos to vote for", required=False)

parser_mass_vote = subparsers.add_parser("massvote", description="Add lots of votes for YouTube videos [WIP]")
parser_mass_vote.add_argument("video", type=str, nargs=1, help="The YouTube video ID to vote for")
parser_mass_vote.add_argument("vote_count", type=int)

parser_test = subparsers.add_parser("print", description="Join room and print received messages to console for debugging")

parser_test = subparsers.add_parser("test", description="")

args = parser.parse_args()

api_key = ""
yt_base_uri = "https://www.googleapis.com/youtube/v3/"
tt_base_uri = "https://togethertube.com/api/v1"
yt_base_args = {"part": "contentDetails", "key": api_key}
tt_base_args = {"mediaServiceId": "youtube"}

tt_websocket = "wss://togethertube.com/websocket/rooms"

def getPlaylistItems(playlistId):
	if args.verbose:
		print("grabbing playlist", playlistId)

	uri = yt_base_uri + "playlistItems"
	uri_args = yt_base_args.copy()
	uri_args["playlistId"] = playlistId
	uri_args["maxResults"] = 50
	playlist = None
	totalItems = None
	while not playlist or "nextPageToken" in playlist.keys():
		if args.verbose:
			print(uri, uri_args)
		if playlist:
			uri_args["pageToken"] = playlist["nextPageToken"]
		r = requests.get(url=uri, params=uri_args)
		try:
			r.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print(playlist)
			raise
		playlist = r.json()
		totalItems = playlist["pageInfo"]["totalResults"]
		for item in playlist["items"]:
			yield item["contentDetails"]["videoId"]

def getChannelVideos(channelId):
	if args.verbose:
		print("grabbing channel's uploads", channelId)

	uri = yt_base_uri + "channels"
	uri_args = yt_base_args.copy()
	uri_args["id"] = channelId
	if args.verbose:
		print(uri, uri_args)
	resp = requests.get(url=uri, params=uri_args)
	uploads_playlist_id = resp.json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
	return getPlaylistItems(uploads_playlist_id)

def getVideosFromReddit(subreddit):
	if args.verbose:
		print("grabbing youtube videos from subreddit", subreddit)

	# TODO: implement

def getPlaySession(roomId):
	"""
	returns PLAY_SESSION cookie so that a websocket connection can be established.
	"""
	uri = "https://togethertube.com/rooms/{}".format(roomId)
	r = requests.get(uri)
	if args.verbose: print("probe room: status code:", r.status_code)
	return r.cookies["PLAY_SESSION"]

class TogetherTubeClient(object):
	"""docstring for TogetherTubeClient."""
	def __init__(self, room, play_session=None):
		super(TogetherTubeClient, self).__init__()
		self.room = room
		if play_session:
			self.play_session = play_session
		else:
			self.play_session = getPlaySession(room)
		self.ws = None
		self.users = [] # TODO
		self.playlistState = None
		self.playerState = None
		self.user_id = None

	def connect(self):
		self.ws = create_connection("{}/{}".format(tt_websocket, self.room), cookie="PLAY_SESSION="+self.play_session)

	def disconnect(self):
		if self.ws:
			self.ws.close()

	def addVote(self, videoId):
		"""
		A websocket connection is required(?) to add votes.
		"""
		global tt_play_session
		uri = "{}/rooms/{}/playlist/votes".format(tt_base_uri, self.room)
		uri_args = tt_base_args
		uri_args["mediaId"] = videoId
		status_code = None
		tries = 0
		while tries < 3 and (not status_code or status_code != 201):
			r = requests.post(uri, json=uri_args, cookies={"PLAY_SESSION":self.play_session, "__uvt":""})
			print("vote: status code:", r.status_code)
			status_code = r.status_code
			tries += 1
			if status_code != 201 and tries < 3:
				time.sleep(0.25 * tries)
				print("retrying...")

	def changeName(self, userId, newName):
		"""
		A websocket connection is required to change name.
		"""
		uri = "{}/users/{}".format(tt_base_uri, userId)
		uri_args = {"name":newName}
		r = requests.put(uri, json=uri_args, cookies={"PLAY_SESSION":self.play_session, "__uvt":""})
		print("change name: status code:", r.status_code)

	def process(self):
		receive = self.ws.recv()
		if args.verbose: print(receive)
		msg = json.loads(receive)
		if msg["id"] == "userList":
			self.users = msg["data"]["users"]
		elif msg["id"] == "userJoined":
			userAccount = msg["data"]["userAccount"]
			if not self.user_id:
				self.user_id = userAccount["id"]
			self.users += [userAccount]
		elif msg["id"] == "playlistState":
			self.playlistState = msg["data"]["playlist"]["items"]
		elif msg["id"] == "playerState":
			self.playerState = msg["data"]["playerState"]
		elif msg["id"] == "systemMessage":
			self.process()

print(args)
if args.action == "massadd":
	client = TogetherTubeClient(args.room)
	client.connect()
	video_num = 1
	videos_queued = 0
	if args.playlist:
		playlist = getPlaylistItems(args.playlist)
	elif args.channel:
		playlist = getChannelVideos(args.channel)
	for video in playlist:
		if video_num >= args.playlist_start:
			print("voting for video", "#"+str(video_num), video, "in", args.room)
			client.addVote(video)
			videos_queued += 1
			video_num += 1
			if args.playlist_length and videos_queued >= args.playlist_length:
				break
		else:
			video_num += 1
	client.disconnect()
elif args.action == "massvote":
	isDone = False

	clients = []
	while len(clients) < args.vote_count:
		clients += [TogetherTubeClient(args.room)]

	for client in clients:
		client.connect()
		client.process()

	for video in args.video:
		isDone = False
		while not isDone:
			for client in clients:
				client.process()
				if client.playerState and client.playerState["mediaId"] == video:
					isDone = True
					break
				print(client.playlistState)
				if client.playlistState and any([vid["media"]["id"] == video for vid in client.playlistState]):
					if args.verbose:
						print("already queued")
				else:
					client.addVote(video)

	for client in clients:
		client.disconnect()
elif args.action == "print":
	client = TogetherTubeClient(args.room)
	client.connect()
	while True:
		args.verbose = True # This enables printing messages to console
		client.process()
elif args.action == "test":
	client = TogetherTubeClient(args.room)
	client.connect()
	while True:
		client.process()
		print("PLAYLIST=", client.playlistState)
