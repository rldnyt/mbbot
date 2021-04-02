import discord
import asyncio
import random
import openpyxl
from discord import Member, Embed
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime

countG = 0
client = discord.Client()
players = {}
queues= {}
musiclist=[]
mCount=1
searchYoutube={}
searchYoutubeHref={}

def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()



@client.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("---------------접속된 서버---------------")
    list = []
    for server in client.servers:
        list.append(server.name)
    print("\n".join(list))
    print("---------------사용기록---------------")
    await client.change_presence(game=discord.Game(name="디스코드 봇 | !명령어 !", type=1))



@client.event
async def on_message(message):
    arg = message.content.split(" ")[0]
    cmd = ["!채팅청소", "!청소", "!챗청"] # "!버킷 청소" 제외
    cmdIgnores = ["!사진찾기", "!사진검색", "!날씨", "!버킷 청소"]
    
    if arg not in cmdIgnores:
        print("--------------------")
        print("청소")
        print("--------------------")
        print(message.author.id)
        print("--------------------")
        print(" ∧ 사용한 사람의 id")
        print(" ∨사용한 사람의 name")
        print("--------------------")
        print(message.author.name)
        print("--------------------")
        print(" ∨사용한 서버")
        print("--------------------")
        print(message.author.server)
        print("--------------------")
        print(" ")
        
    if arg in cmd:
        tmp = await client.send_message(message.channel, "청소시작....")
        async for msg in client.logs_from(message.channel):
            await client.delete_message(msg)

    elif arg == "!명령어":
        embed = discord.Embed(
            title = "퐈퐈봇 명령어",
            description ="퐈퐈봇 명령어입니다.",
            colour = discord.Colour.blue()
        )
        embed.add_field(name="!채팅청소 or !청소 or !챗청", value="채팅방의 글을 청소 합니다.(채팅삭제한 기록은 봇 작동하는곳에 남습니다.)", inline=False)
        embed.add_field(name="!명령어", value="퐈퐈봇의 명령어을 확인합니다", inline=False)
        embed.add_field(name="!제작자", value="퐈퐈봇을 만든 제작진을 알아봄니다", inline=False)
        embed.add_field(name="!사진찾기[검색 할거] or !사진검색 [검색 할거]", value="랜덤으로 사진을 검색하여 보여줌니다.", inline=False)
        embed.add_field(name="!모두모여", value="모두에게 알림을 보냅니다.", inline=False)
        embed.add_field(name="!봇이종료되었어요", value="봇종료시 어떻게해야하는지 알려줌니다.", inline=False)
        embed.add_field(name="!투표 투표주제/선택할 항목", value="투표을 합니다(예 : !투표 내가 좋아하는것은?/사과/안녕/구독", inline=False)
        embed.add_field(name="!날씨 [지역]", value="그 지역에 날씨을 알려줌니다, 이상한 날씨을 알려주라고 하면퐈퐈가 무시합니다!", inline=False)
        embed.add_field(name="!서버", value="퐈퐈봇을 사용중인 서버을 알려줌니다.", inline=False)
        embed.add_field(name="!내 정보", value="자신의 정보을 보여줌니다.", inline=False)
        embed.add_field(name="-----------(일정 기능은 작동안함니당(재생에 검색어재생기능,재생목록삭제, 곡설명, 소리)", value="음성 관련", inline=False)
        embed.add_field(name="!들어와", value="퐈퐈가 음성채널에 입장합니다", inline=False)
        embed.add_field(name="!나가", value="퐈퐈가 음성채널에서 나감니다.", inline=False)
        embed.add_field(name="!재생 [재생할유튜브영상링크/검색어]", value="노래을 재생합니다.", inline=False)
        embed.add_field(name="!일시정지", value="노래을 일시정지합니다", inline=False)
        embed.add_field(name="!다시재생", value="노래을 다시재생합니다", inline=False)
        embed.add_field(name="!멈춰", value="노래을 멈춤니다.", inline=False)
        embed.add_field(name="!재생목록삭제", value="재생목록을 삭제합니다.", inline=False)
        embed.add_field(name="!소리 <수치>  <+ / ->", value="불륨을 조절합니다.", inline=False)
        embed.add_field(name="!곡설명", value="재생목록을 확입합니다.", inline=False)

        await message.channel.send(embed=embed)
        await message.channel.send("업대이트내용은 : https://discord.gg/6Rxcwwb 에서확인해세요!")

    elif arg == "!제작자":
        file = openpyxl.load_workbook("퐘퐘제작자.xlsx")
        sheet = file.active
        memory = message.content.split(" ")
        for i in range(1, 5):
            await client.send_message(message.channel, sheet["A" + str(i)].value)
            break

    elif arg == "!모두모여":
        await client.send_message(message.channel, "@everyon")

    elif arg == "!들어와":
        channel = message.author.voice.voice_channel
        server = message.server
        voice_client = client.voice_client_in(server)
        if voice_client == None:
            await client.send_message(message.channel, "들어왔습니다")  # 호오.... 나를 부르는건가? 네녀석.. 각오는 되있겠지?
            await client.join_voice_channel(channel)
        else:
            await client.send_message(message.channel, "봇이 이미 들어와있습니다.")  # 응 이미 들어와있어 응쓰게싸

    elif arg == "!나가":
        server = message.server
        voice_client = client.voice_client_in(server)
        if voice_client == None:
            await client.send_message(message.channel, "봇이 음성채널에 접속하지 않았습니다.")  # 원래나가있었음 바보녀석 니녀석의 죄는 "어리석음" 이라는 .것.이.다.
            pass
        else:
            await client.send_message(message.channel, "나갑니다")  # 나가드림
            await voice_client.disconnect()

    elif arg == "!재생":
        server = message.server
        voice_client = client.voice_client_in(server)
        msg1 = message.content.split(" ")
        url = msg1[1]
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        players[server.id] = player
        await client.send_message(message.channel, embed=discord.Embed(description="노래을 재생합니다."))
        player.start()

    elif arg == "!일시정지":
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="노래을 일시정지을하였습니다, 다시재생은 !다시재생"))
        players[id].pause()

    elif arg == "!다시재생":
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="다시재생을합니다."))
        players[id].resume()

    elif arg == "!멈춰":
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="노래가 리셋되었습니다 새로운 음악은 !재생[유튜브링크]"))
        players[id].stop()

    elif arg == "!사진찾기" or arg == "!사진검색":
        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]
        print(Text.strip())  # 입력한 명령어

        randomNum = random.randrange(0, 40)  # 랜덤 이미지 숫자

        location = Text
        enc_location = urllib.parse.quote(location)  # 한글을 url에 사용하게끔 형식을 바꿔줍니다. 그냥 한글로 쓰면 실행이 안됩니다.
        hdr = {"User-Agent": "Mozilla/5.0"}
        url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=" + enc_location  # 이미지 검색링크+검색할 키워드
        print(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")  # 전체 html 코드를 가져옵니다.
        # print(bsObj)
        imgfind1 = bsObj.find("div", {"class": "photo_grid _box"})  # bsjObj에서 div class : photo_grid_box 의 코드를 가져옵니다.
        # print(imgfind1)
        imgfind2 = imgfind1.findAll("a", {"class": "thumb _thumb"})  # imgfind1 에서 모든 a태그 코드를 가져옵니다.
        imgfind3 = imgfind2[randomNum]  # 0이면 1번째사진 1이면 2번째사진 형식으로 하나의 사진 코드만 가져옵니다.
        imgfind4 = imgfind3.find("img")  # imgfind3 에서 img코드만 가져옵니다.
        imgsrc = imgfind4.get("data-source")  # imgfind4 에서 data-source(사진링크) 의 값만 가져옵니다.
        print(imgsrc)
        embed = discord.Embed(
            colour=discord.Colour.green()
        )
        embed.add_field(name="검색 : " + Text, value="링크 : " + imgsrc, inline=False)
        embed.set_image(url=imgsrc)  # 이미지의 링크를 지정해 이미지를 설정합니다.
        await client.send_message(message.channel, embed=embed)  # 메시지를 보냅니다.
        print("--------------------")
        print(" ")

    elif arg == "!봇이종료되었어요":
        channel = message.channel
        embed = discord.Embed(
            colour=discord.Colour.green()
        )

        embed.add_field(name="💎봇이 종료되었을때는 관리자에게 디스코드!", value="기우YT#2997 또는 기우태블릿MB+#3647 으로 연락부탁!", inline=False)
        embed.add_field(name="또는 아래 디스코드방 봇이-좋료-되었어요 에 알려주세요!", value="https://discord.gg/6Rxcwwb", inline=False)

        await client.send_message(channel, embed=embed)

    elif arg == "!투표":
        vote = message.content[4:].split("/")
        await client.send_message(message.channel, "❗투표주제 - " + vote[0])
        for i in range(1, len(vote)):
            choose = await client.send_message(message.channel, "```" + vote[i] + "```")
            await client.add_reaction(choose, "☮")

    elif arg == "!날씨":
        print("--------------------")
        print("날씨")
        print("--------------------")
        print(message.author.id)
        print("--------------------")
        print(" ∧ 사용한 사람의 id")
        print(" ∨사용한 사람의 name")
        print("----------------------------------")
        print(message.author.name)
        print("--------------------")
        print(" ∨사용한 서버")
        print("--------------------")
        print(message.author.server)
        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location + "날씨")
        hdr = {"User-Agent": "Mozilla/5.0"}
        url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=" + enc_location
        print("--------------------")
        print(url)
        print("--------------------")
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find("div", {"class": "main_info"})

        todayTemp1 = todayBase.find("span", {"class": "todaytemp"})
        todayTemp = todayTemp1.text.strip()  # 온도
        print(todayTemp)
        print("--------------------")

        todayValueBase = todayBase.find("ul", {"class": "info_list"})
        todayValue2 = todayValueBase.find("p", {"class": "cast_txt"})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        print(todayValue)
        print("--------------------")

        todayFeelingTemp1 = todayValueBase.find("span", {"class": "sensible"})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도
        print(todayFeelingTemp)
        print("--------------------")

        todayMiseaMongi1 = bsObj.find("div", {"class": "sub_info"})
        todayMiseaMongi2 = todayMiseaMongi1.find("div", {"class": "detail_box"})
        todayMiseaMongi3 = todayMiseaMongi2.find("dd")
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지
        print(todayMiseaMongi)
        print("--------------------")

        tomorrowBase = bsObj.find("div", {"class": "table_info weekly _weeklyWeather"})
        tomorrowTemp1 = tomorrowBase.find("li", {"class": "date_info"})
        tomorrowTemp2 = tomorrowTemp1.find("dl")
        tomorrowTemp3 = tomorrowTemp2.find("dd")
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
        print(tomorrowTemp)
        print("--------------------")

        tomorrowAreaBase = bsObj.find("div", {"class": "tomorrow_area"})
        tomorrowMoring1 = tomorrowAreaBase.find("div", {"class": "main_info morning_box"})
        tomorrowMoring2 = tomorrowMoring1.find("span", {"class": "todaytemp"})
        tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
        print(tomorrowMoring)
        print("--------------------")

        tomorrowValue1 = tomorrowMoring1.find("div", {"class": "info_data"})
        tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
        print(tomorrowValue)
        print("--------------------")

        tomorrowAreaBase = bsObj.find("div", {"class": "tomorrow_area"})
        tomorrowAllFind = tomorrowAreaBase.find_all("div", {"class": "main_info morning_box"})
        tomorrowAfter1 = tomorrowAllFind[1]
        tomorrowAfter2 = tomorrowAfter1.find("p", {"class": "info_temperature"})
        tomorrowAfter3 = tomorrowAfter2.find("span", {"class": "todaytemp"})
        tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
        print(tomorrowAfterTemp)
        print("--------------------")

        tomorrowAfterValue1 = tomorrowAfter1.find("div", {"class": "info_data"})
        tomorrowAfterValue = tomorrowAfterValue1.text.strip()

        print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지
        print("----------------------------------")
        print("   ")

        embed = discord.Embed(
            title=learn[1] + " 의 날씨 정보",
            description=learn[1] + "의 날씨 정보입니다.",
            colour=discord.Colour.dark_blue()
        )
        embed.add_field(name="현재온도", value=todayTemp + "˚", inline=False)  # 현재온도
        embed.add_field(name="체감온도", value=todayFeelingTemp, inline=False)  # 체감온도
        embed.add_field(name="현재상태", value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        embed.add_field(name="현재 미세먼지 상태", value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
        embed.add_field(name="오늘 오전/오후 날씨", value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
        embed.add_field(name="**----------------------------------**", value="**----------------------------------**",
                        inline=False)  # 구분선
        embed.add_field(name="내일 오전온도", value=tomorrowMoring + "˚", inline=False)  # 내일오전날씨
        embed.add_field(name="내일 오전날씨상태, 미세먼지 상태", value=tomorrowValue, inline=False)  # 내일오전 날씨상태
        embed.add_field(name="내일 오후온도", value=tomorrowAfterTemp + "˚", inline=False)  # 내일오후날씨
        embed.add_field(name="내일 오후날씨상태, 미세먼지 상태", value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태

        await client.send_message(message.channel, embed=embed)

    elif arg == "!버킷 청소"):
        for index in range(21):
            print(" ")
        print("---------------사용기록---------------")
        print(" ")
        print("--------------------")
        print("버킷 기록 청소")
        print("--------------------")
        print(message.author.id)
        print("--------------------")
        print(" ∧ 사용한 사람의 id")
        print(" ∨사용한 사람의 name")
        print("--------------------")
        print(message.author.name)
        print("--------------------")
        print(" ∨사용한 서버")
        print("--------------------")
        print(message.author.server)
        print("--------------------")
        print(" ")

    elif arg == "!서버"):
        list = []
        for server in client.servers:
            list.append(server.name)
        await client.send_message(message.channel, embed=discord.Embed(description="\n".join(list)))


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
