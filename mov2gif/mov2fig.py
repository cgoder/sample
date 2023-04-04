from moviepy.editor import VideoFileClip

input = 'hannah.mp4'
videoclip = VideoFileClip(input)

# 移除音频
videoclip = videoclip.without_audio()

# 倍速
newClip = videoclip.speedx(4)
newClip.write_videofile('4x.mp4')
# 保存第1帧
videoclip.save_frame("frame1.jpg")
# 保存4s时刻的那1帧
videoclip.save_frame("frame4.png", t=4) 
# 2gif,5fps
output = '5fps.gif'
newClip.write_gif(output,fps=5)
