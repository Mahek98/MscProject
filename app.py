# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:26:01 2023

@author: 91983
"""

from flask import Flask,jsonify, render_template, request,send_from_directory,send_file,session
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googleapiclient.discovery import build
import os
import yt_dlp
import moviepy.editor as mp
from moviepy.editor import AudioFileClip
from collections import Counter
import pickle
import pvleopard
from typing import Sequence, Optional
from moviepy.editor import VideoFileClip, TextClip
from moviepy.editor import concatenate_videoclips
import nltk


app = Flask(__name__)
customize=None
video_filename = None
preference=None
danceStyleInput=None
danceLevelInput=None
audio=None
word_to_find=None
subtitle_video = None
key_moments_list=None

@app.route('/', methods=['GET', 'POST'])
def index():
    global video_filename
    output_directory = r'D:/Msc Project'
    if request.method == 'POST':
        customize = request.form['customize']
        duration = int(request.form['duration'])
        duration = duration * 60
        danceStyleInput = request.form['danceStyleInput']
        danceLevelInput = request.form['danceLevelInput']
        word_to_find = request.form['word_to_find']
        audio=request.form['audio']
        video_urls,video_id = search_youtube_videos(customize,danceStyleInput,danceLevelInput, output_directory)
        downloaded_videos,subtitle_video = download_youtube_video(video_urls, output_directory,word_to_find,video_id)
        if audio:
            audio_url=search_audio_url(audio)
            downloaded_audios=download_song(audio_url,output_directory)
            file_path,final_audio=extract_audio(downloaded_audios[0])
        if downloaded_videos:
            merged_videos = []
            for video_filename in downloaded_videos:
                video_path = os.path.join(output_directory, video_filename)

                if os.path.exists(video_path):
                    if subtitle_video:
                        merged_video_filename = merge_and_trim_specific_parts(subtitle_video, duration, output_directory)
                    else:
                        merged_video_filename = merge_and_trim_specific_parts(video_filename, duration, output_directory)
                    if merged_video_filename:
                        trimmed_video_path=os.path.join(output_directory, merged_video_filename)
                        if audio:
                            merged_audio_video_path=merge_audio_with_video(trimmed_video_path,downloaded_audios[0],output_directory)
                            final_video_path = os.path.join('videos', merged_audio_video_path).replace('\\', '/')
                            return render_template('index.html', video_src=final_video_path)
                        else:
                            final_video_path = os.path.join('videos', merged_video_filename).replace('\\', '/')
                            return render_template('index.html', video_src=final_video_path)
                    else:
                        return render_template('index.html', video_src=None)
                else:
                    return render_template('index.html', video_src=None)
        else:
            print("No videos available")
            return render_template('index.html', video_src=None)
        
    else:
        customize = None
        return render_template('index.html', video_src=None)


@app.route('/videos/<filename>')
def videos(filename):
    return send_from_directory(output_directory, filename)


def download_youtube_video(video_url,output_path,word_to_find,video_id):
    downloaded_videos = [] 
    options = {
        'format': 'best',
        'outtmpl': 'D:/Msc Project/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        # 'writeinfojson': True, 
        'writesubtitles': True,  # Enable subtitle download
        'writesubtitleslangs': ['en'], 
    }
    for url in video_url:
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                ydl.download([url])
                video_title = info.get('title', 'Untitled') 
                video_filename = f"D:/Msc Project/{video_title}.mp4"  
                options['outtmpl'] = video_filename 
                video_path = os.path.join(output_path, video_filename)
                downloaded_videos.append(video_filename)
                if word_to_find:
                    downloaded_audios=[]
                    downloaded_audios=download_audio_from_video(url,output_directory)
                    file_path,final_audio=extract_audio(downloaded_audios[0])
                    subtitle_path=generate_subtitles(file_path,output_directory,video_id,video_title)
                    subtitle_video=merge_subtitles_with_video(video_path, subtitle_path, output_directory,word_to_find)
                else:
                    subtitle_video=None
                
        except Exception as e:
            print("Error occurred while downloading the video:", e)        
    return downloaded_videos,subtitle_video       

def check_word_similarity(word, block_of_words):
    pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
    if isinstance(block_of_words, str):
        return re.search(pattern, block_of_words) is not None
    elif isinstance(block_of_words, list):
        return any(re.search(pattern, word) is not None for word in block_of_words)
    else:
        return False


def search_youtube_videos(customize,danceStyleInput,danceLevelInput, output_directory):
    
    
    # Tokenize the user customize
    downloaded_videos = []
    tokens = word_tokenize(customize)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Set up YouTube Data API client
    api_key = "AIzaSyCXe5yoUlsLw7uDQAwBlwE8ziBQvKXlbYw"
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Convert the processed tokens into a single string
    processed_text = ' '.join(tokens)

    tokens.append(danceStyleInput.lower())
    tokens.append(danceLevelInput.lower())
    
    tokens.append("tutorial")
    tokens.append("steps")
    tokens.append("guide")
    tokens.append("learn")
    

    # Search for videos based on processed user customize
    search_response = youtube.search().list(
        q=' '.join(tokens),
        part='id',
        maxResults=1 # Increase the number of results to retrieve
    ).execute()

    # Extract video URLs from search results
    video_urls = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_urls.append(f"https://www.youtube.com/watch?v={search_result['id']['videoId']}")
     
    for url in video_urls:
        print(url)
    
    # Filter videos based on dance tutorial criteria
    filtered_video_urls = []
    for url in video_urls:
        video_id = url.split('=')[1]
        video_info = youtube.videos().list(part='snippet', id=video_id).execute()
        video_title = video_info['items'][0]['snippet']['title'].lower()
        video_description = video_info['items'][0]['snippet']['description'].lower()
        video_tags = video_info['items'][0]['snippet'].get('tags', [])
        word_to_check1="Bollywood"
        word_to_check2="Dance"
        word_to_check3="Hip Hop"
        word_to_check4="contemporary"
        # Check if the video indicates tutorial content
        if (check_word_similarity(word_to_check1, video_title)) and (check_word_similarity(word_to_check2, video_title)) or (check_word_similarity(word_to_check3, video_title)) and (check_word_similarity(word_to_check2, video_title)) or (check_word_similarity(word_to_check4, video_title)) and (check_word_similarity(word_to_check2, video_title)):
            if check_word_similarity('tutorial', video_title) or check_word_similarity('tutorial', video_description):
                filtered_video_urls.append(url)
            elif any(check_word_similarity(keyword, video_title) for keyword in ['learn', 'step-by-step', 'how to', 'guide', 'instructional']):
                filtered_video_urls.append(url)
            elif any(check_word_similarity(keyword, video_description) for keyword in ['learn', 'step-by-step', 'how to', 'guide', 'instructional']):
                filtered_video_urls.append(url)
            elif any(check_word_similarity(keyword, video_tags) for keyword in ['tutorial', 'lesson', 'instruction']):
                filtered_video_urls.append(url)
            elif any(check_word_similarity(keyword, video_tags) for keyword in tokens):
                filtered_video_urls.append(url)
            else:
                return "Search prefernece not matched"
            filtered_video_urls.append(url)
            
    # After the search, display the most used dance style, dance level, and preference words
    print("filtered_video_urls")
    print(filtered_video_urls)

    return filtered_video_urls,video_id

def merge_and_trim_specific_parts(video_urls, duration, output_directory):

    print("in merge and trim specifc parts video path")
    print(video_urls)
    merged_video = merge_videos(video_urls, output_directory)
    final_video = trim_video(merged_video, duration, output_directory)
    return final_video

def merge_videos(video_urls, output_directory):
    video_clips = []

    video_clip = mp.VideoFileClip(video_urls)
    video_clips.append(video_clip)
    
    merged_video = mp.concatenate_videoclips(video_clips)
    
    return merged_video

def trim_video(video, duration, output_directory):
    start_time = 0  # Start time for trimming 
    end_time = start_time + duration  # End time for trimming
    trimmed_video = video.subclip(start_time, end_time)

    trimmed_video_filename = f"trimmed_video_{duration}s.mp4"
    trimmed_video_path = os.path.join(output_directory, trimmed_video_filename).replace('\\', '/')
    trimmed_video.write_videofile(trimmed_video_path)
    return trimmed_video_filename


def search_audio_url(audio):

    api_key = "AIzaSyCXe5yoUlsLw7uDQAwBlwE8ziBQvKXlbYw"
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        search_response = youtube.search().list(
            q=audio,
            part='id',
            type='video',
            maxResults=1
        ).execute()
        video_id = search_response['items'][0]['id']['videoId']
        audio_urls=[]
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                audio_urls.append(f"https://www.youtube.com/watch?v={search_result['id']['videoId']}")
        return audio_urls

    except Exception as e:
        print("An error occurred:", e)


def download_audio_from_video(url, output_path):
    downloaded_videos = []
    print("in download song url")
    print(url)
    
    # Specify options for the video download
    options = {
        'format': 'best',
        'outtmpl': 'D:/Msc Project/video1.mp3',
        'merge_output_format': 'mp4',
        'writeinfojson': True,  # Write video metadata to a JSON file
    }
    

    try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False) 
                ydl.download([url])
                video_title = info.get('title', 'Untitled') 
                video_filename = f"D:/Msc Project/video1.mp3" 
                downloaded_videos.append(video_filename)
                
    except Exception as e:
            print("Error occurred while downloading the video:", e)
    return downloaded_videos



def download_song(video_url, output_path):
    downloaded_videos = []
    print("in download song url")
    print(video_url)
    
    # Specify options for the video download
    options = {
        'format': 'best',
        'outtmpl': 'D:/Msc Project/video1.mp3',
        'merge_output_format': 'mp4',
        'writeinfojson': True,  # Write video metadata to a JSON file
    }
    
    for url in video_url:
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False) 
                ydl.download([url])
                video_title = info.get('title', 'Untitled') 
                video_filename = f"D:/Msc Project/video1.mp3" 
                downloaded_videos.append(video_filename)
                
        except Exception as e:
            print("Error occurred while downloading the video:", e)
    return downloaded_videos

  
def extract_audio(url):

    try:
      
       audio_clip = mp.VideoFileClip(url)
       output_file = r"D:/Msc Project/trimmed_audio.mp3"
       audio_clip.audio.write_audiofile(output_file)
       return output_file,audio_clip
    except Exception as e:
        print("error occured in audio extraction")
        print(e)
        return None

def merge_audio_with_video(video_path, audio_path, output_path):

    video_path=video_path.replace('\\', '/')
    video_clip = VideoFileClip(video_path)

    # Load the audio clip
    audio_path=audio_path.replace('\\', '/')
    print(audio_path)
    audio_clip = AudioFileClip(audio_path)

    video_clip = video_clip.set_audio(audio_clip)

    op_path = "final.mp4"
    video_clip.write_videofile(op_path, codec="libx264", audio_codec="aac")
	

    return op_path

# Call the function with the preference variable
output_directory = r'D:/Msc Project'


def generate_subtitles(url,output_directory,video_id,video_title):
    leopard = pvleopard.create(access_key="/cnO/o9TNcOqOHuyJzj+rgUYAOkIrEEzLKf1IIKycelikVAEiXbkSg==")
    transcript, words = leopard.process_file(url)
    filename = "subtitle.srt"
    filename_path = os.path.join(output_directory, filename).replace('\\', '/')
    subtitle_path=filename_path
    with open(subtitle_path, 'w') as f:
        f.write(to_srt(words))
    
    extract_key_moments(subtitle_path)
    return subtitle_path


def second_to_timecode(x: float) -> str:
        hour, x = divmod(x, 3600)
        minute, x = divmod(x, 60)
        second, x = divmod(x, 1)
        millisecond = int(x * 1000.)
    
    
        return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)
    
def to_srt(
            words: Sequence[pvleopard.Leopard.Word],
            endpoint_sec: float = 1.,
            length_limit: Optional[int] = 16) -> str:
        def _helper(end: int) -> None:
            lines.append("%d" % section)
            lines.append(
                "%s --> %s" %
                (
                    second_to_timecode(words[start].start_sec),
                    second_to_timecode(words[end].end_sec)
                )
            )
            lines.append(' '.join(x.word for x in words[start:(end + 1)]))
            lines.append('')

        lines = list()
        section = 0
        start = 0
        for k in range(1, len(words)):
            if ((words[k].start_sec - words[k - 1].end_sec) >= endpoint_sec) or \
                    (length_limit is not None and (k - start) >= length_limit):
                _helper(k - 1)
                start = k
                section += 1
        _helper(len(words) - 1)
    
        
        return '\n'.join(lines)



def extract_key_moments(subtitle_file):
    with open(subtitle_file, 'r') as file:
        subtitles = file.read()
    subtitle_parts = subtitles.split('\n\n')

    # Create a set of stopwords to filter out common words
    stop_words = set(stopwords.words('english'))

    # Create a list to store extracted portions for each key moment
    key_moments_list = []

    for part in subtitle_parts:
        lines = part.split('\n')
        if len(lines) >= 3:
            timestamp_line = lines[1]
            title = lines[2]

            # Tokenize the title and filter out stopwords
            words = nltk.word_tokenize(title.lower())
            main_words = [word for word in words if word.isalpha() and word not in stop_words]

            # Get the most common words to represent the key moment
            word_counts = Counter(main_words)
            most_common_words = word_counts.most_common(3)  # You can adjust the number of words to keep (e.g., 3)

            # Concatenate the most common words to form a portion
            portion = ' '.join(word for word, _ in most_common_words)
            if portion:
                start_time, _, _ = timestamp_line.partition(' --> ')
                key_moments_list.append(f"{start_time} - {portion}")
                
    print("key_moments_list")
    print(key_moments_list)
    return "\n".join(key_moments_list)


def merge_subtitles_with_video(video_path, subtitle_path, output_path,word_to_find):
  
   video_path=video_path.replace('\\', '/')

   video_clip = VideoFileClip(video_path)
   
   try:
       with open(subtitle_path, 'r') as f:
           subtitle_lines = f.readlines()
       for i, line in enumerate(subtitle_lines):
           line = line.strip()
           if re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):  # Match timestamps in SRT format
               subtitle = ' '.join(subtitle_lines[i+1:i+3]).strip()
               if word_to_find.lower() in subtitle.lower():
                   start_time, _ = re.findall(r'\d+:\d+:\d+,\d+', line)
                   start_time_seconds = convert_to_seconds(start_time)
                   video_clip = video_clip.subclip(start_time_seconds)
                   break
              
   except Exception as e:
     print("error in merging",e)
     return            

   sub_video_filename = "subtitlegenerated.mp4"
   sub_video_path = os.path.join(output_path, sub_video_filename).replace('\\', '/')
   output_path=sub_video_path
   video_clip.write_videofile(output_path, codec="libx264")
   video_clip.close()
   return output_path
   


def convert_to_seconds(time_str):
    time_str = str(time_str)  # Ensure time_str is converted to a string
    time_str = time_str.replace(',', '.')  # Replace comma with period for milliseconds
    hours, minutes, seconds = time_str.split(':')
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


if __name__ == "__main__":
    app.run()