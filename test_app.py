# # -*- coding: utf-8 -*-
# """
# Created on Thu Jul 13 13:06:45 2023

# @author: 91983
# """

import pytest

import app


def test_video_search1():
    customize = "foot steps"  # The search query for the test
    danceStyleInput = "bollywood"
    danceLevelInput = "easy"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""
    

def test_video_search2():
    customize = "bhangra"  # The search query for the test
    danceStyleInput = "bollywood"
    danceLevelInput = "easy"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""

        
def test_video_search3():
    customize = "foot steps"  # The search query for the test
    danceStyleInput = "hip hop"
    danceLevelInput = "easy"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""

def test_video_search4():
    customize = "kick ball change"  # The search query for the test
    danceStyleInput = "hip hop"
    danceLevelInput = "easy"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""


def test_video_search5():
    customize = "foot steps"  # The search query for the test
    danceStyleInput = "contemporary"
    danceLevelInput = "easy"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""
    

def test_video_search6():
    customize = "axle "  # The search query for the test
    danceStyleInput = "contemporary"
    danceLevelInput = "easy"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""

def test_video_search7():
    customize = "footwork"  # The search query for the test
    danceStyleInput = "bollywood"
    danceLevelInput = "medium"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""

def test_video_search8():
    customize = "spins"  # The search query for the test
    danceStyleInput = "contemporary"
    danceLevelInput = "medium"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""
    

def test_video_search10():
    customize = "footwork"  # The search query for the test
    danceStyleInput = "bollywood"
    danceLevelInput = "hard"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""

def test_video_search11():
    customize = "spins"  # The search query for the test
    danceStyleInput = "contemporary"
    danceLevelInput = "hard"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""
    
def test_video_search12():
    customize = "footwork"  # The search query for the test
    danceStyleInput = "hip hop"
    danceLevelInput = "hard"
    output_directory = "D:/Msc Project"
    video_url = app.search_youtube_videos(customize, danceStyleInput, danceLevelInput, output_directory)

    # Verify that the video URL is not empty or None
    assert video_url is not None and video_url != ""
    
   

def test_audio_search1():   
    test_audio_name="Baarishein"
    audio_url=app.search_audio_url(test_audio_name)
    # Verify that the video URL is not empty or None
    assert audio_url is not None and audio_url != ""
    
def test_audio_search2():   
    test_audio_name="So cold"
    audio_url=app.search_audio_url(test_audio_name)
    # Verify that the video URL is not empty or None
    assert audio_url is not None and audio_url != ""
    
def test_audio_search3():   
    test_audio_name="Calm Down"
    audio_url=app.search_audio_url(test_audio_name)
    # Verify that the video URL is not empty or None
    assert audio_url is not None and audio_url != ""
    
def test_download1():
    video_url=[]
    video_url.append("https://www.youtube.com/watch?v=mVhfaPpxDkw&t=27s")
    output_path="D:/Msc Project"
    word_to_find="shoulders"
    video_id="mVhfaPpxDkw&t=27s"
    video_result=app.download_youtube_video(video_url,output_path,word_to_find,video_id)
    # Verify that the video URL is not empty or None
    assert video_result is not None and video_result != ""
    
def test_download2():
    video_url=[]
    video_url.append("https://www.youtube.com/watch?v=mVhfaPpxDkw&t=27s")
    output_path="D:/Msc Project"
    word_to_find=None
    video_id="mVhfaPpxDkw&t=27s"
    video_result=app.download_youtube_video(video_url,output_path,word_to_find,video_id)
    # Verify that the video URL is not empty or None
    assert video_result is not None and video_result != ""

def test_word_similarity():
    word="Bollywood"
    block_of_words=["bollywood","dance","routine"]
    similarity_result=app.check_word_similarity(word,block_of_words)
    assert similarity_result is not None and similarity_result != ""

def test_merging():
    # add title here below before testing
    video_urls="D:/Msc Project/{video_title}.mp4"  
    duration=1
    output_directory="D:/Msc Project"
    merging_result=app.merge_and_trim_specific_parts(video_urls, duration, output_directory)
    assert merging_result is not None and merging_result != ""

def test_download_audio_from_video():
    url=[]
    url.append("https://www.youtube.com/watch?v=mVhfaPpxDkw&t=27s")
    output_path="D:/Msc Project"
    av_result=app.download_audio_from_video(url, output_path)
    assert av_result is not None and av_result != ""
    
def test_merge_audio_with_video():
    video_path="add local system path"
    audio_path="add local system path"
    output_path="D:/Msc Project"
    merge_result=app.merge_audio_with_video(video_path, audio_path, output_path)
    assert merge_result is not None and merge_result != ""

def test_generate_subtitles():
    url="add path"
    output_directory="D:/Msc Project"
    video_id="add path"
    video_title="add path"
    subtitle_result=app.generate_subtitles(url,output_directory,video_id,video_title)
    assert subtitle_result is not None and subtitle_result != ""

    
def test_merge_subtitles_with_video():
    video_path="add path"
    subtitle_path="add path"
    output_path="D:/Msc Project"
    word_to_find="shoulders"
    merge_result=app.merge_subtitles_with_video(video_path, subtitle_path, output_path,word_to_find)
    assert merge_result is not None and merge_result != ""

    
# Run the tests
if __name__ == "__main__":
    pytest.main()