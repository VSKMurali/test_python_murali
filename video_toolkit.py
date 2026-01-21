import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import os
from pathlib import Path
import subprocess
import shutil


class VideoToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Toolkit Pro")
        self.root.geometry("900x750")
        self.root.configure(bg="#1e1e2e")

        self.video_path = None
        self.video = None
        self.total_frames = 0
        self.fps = 0
        self.duration = 0
        self.current_position = 0
        self.ffmpeg_path = None
        self.merge_video_list = []

        # Try to find ffmpeg
        self.find_ffmpeg()

        self.setup_ui()

    def find_ffmpeg(self):
        """Find FFmpeg executable in system PATH or common locations"""
        # First try system PATH
        self.ffmpeg_path = shutil.which('ffmpeg')

        if self.ffmpeg_path:
            return

        # Common Windows locations
        common_paths = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            os.path.expanduser(r"~\Downloads\ffmpeg-*\bin\ffmpeg.exe"),
        ]

        # Search in Downloads folder
        downloads_folder = os.path.expanduser("~\\Downloads")
        if os.path.exists(downloads_folder):
            for item in os.listdir(downloads_folder):
                if item.startswith("ffmpeg"):
                    potential_path = os.path.join(downloads_folder, item, "bin", "ffmpeg.exe")
                    if os.path.exists(potential_path):
                        self.ffmpeg_path = potential_path
                        return

        # Check common paths
        for path in common_paths:
            if os.path.exists(path):
                self.ffmpeg_path = path
                return

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2e3440", height=60)
        header.pack(fill=tk.X, pady=(0, 10))

        title_label = tk.Label(header, text="🎬 Video Toolkit Pro",
                               font=("Arial", 20, "bold"),
                               bg="#2e3440", fg="#88c0d0")
        title_label.pack(pady=15)

        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg="#2e3440", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # File selection
        file_frame = tk.LabelFrame(left_panel, text="Video File",
                                   bg="#2e3440", fg="#d8dee9",
                                   font=("Arial", 10, "bold"))
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        self.file_label = tk.Label(file_frame, text="No file selected",
                                   bg="#2e3440", fg="#81a1c1",
                                   wraplength=250)
        self.file_label.pack(pady=5)

        select_btn = tk.Button(file_frame, text="Select Video",
                               command=self.select_video,
                               bg="#5e81ac", fg="white",
                               font=("Arial", 10, "bold"),
                               cursor="hand2")
        select_btn.pack(pady=5)

        # Video info
        info_frame = tk.LabelFrame(left_panel, text="Video Information",
                                   bg="#2e3440", fg="#d8dee9",
                                   font=("Arial", 10, "bold"))
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.info_text = tk.Text(info_frame, height=6, bg="#3b4252",
                                 fg="#eceff4", font=("Courier", 9),
                                 relief=tk.FLAT)
        self.info_text.pack(padx=5, pady=5)
        self.info_text.insert("1.0", "Load a video to see details...")
        self.info_text.config(state=tk.DISABLED)

        # Features
        features_frame = tk.LabelFrame(left_panel, text="Features",
                                       bg="#2e3440", fg="#d8dee9",
                                       font=("Arial", 10, "bold"))
        features_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a canvas with scrollbar for features
        canvas = tk.Canvas(features_frame, bg="#2e3440", highlightthickness=0)
        scrollbar = ttk.Scrollbar(features_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2e3440")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        scrollbar.pack(side="right", fill="y")

        # Frame extraction
        extract_frame = tk.Frame(scrollable_frame, bg="#2e3440")
        extract_frame.pack(fill=tk.X, pady=10, padx=5)

        tk.Label(extract_frame, text="Extract Frame at (sec):",
                 bg="#2e3440", fg="#d8dee9", font=("Arial", 9)).pack()

        self.second_entry = tk.Entry(extract_frame, bg="#3b4252",
                                     fg="#eceff4", justify=tk.CENTER)
        self.second_entry.pack(pady=5)
        self.second_entry.insert(0, "0")

        btn_frame = tk.Frame(extract_frame, bg="#2e3440")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Preview",
                  command=self.preview_frame,
                  bg="#81a1c1", fg="white",
                  font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=2)

        tk.Button(btn_frame, text="Extract Frame",
                  command=self.extract_frame,
                  bg="#a3be8c", fg="white",
                  font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=2)

        # Create GIF
        gif_frame = tk.Frame(scrollable_frame, bg="#2e3440")
        gif_frame.pack(fill=tk.X, pady=10, padx=5)

        tk.Label(gif_frame, text="Create GIF:",
                 bg="#2e3440", fg="#d8dee9").pack()

        time_frame = tk.Frame(gif_frame, bg="#2e3440")
        time_frame.pack()

        tk.Label(time_frame, text="From:", bg="#2e3440",
                 fg="#d8dee9").grid(row=0, column=0)
        self.gif_start = tk.Entry(time_frame, width=5, bg="#3b4252",
                                  fg="#eceff4")
        self.gif_start.grid(row=0, column=1, padx=2)
        self.gif_start.insert(0, "0")

        tk.Label(time_frame, text="To:", bg="#2e3440",
                 fg="#d8dee9").grid(row=0, column=2, padx=(5, 0))
        self.gif_end = tk.Entry(time_frame, width=5, bg="#3b4252",
                                fg="#eceff4")
        self.gif_end.grid(row=0, column=3, padx=2)
        self.gif_end.insert(0, "3")

        tk.Button(gif_frame, text="Create GIF",
                  command=self.create_gif,
                  bg="#b48ead", fg="white",
                  font=("Arial", 9, "bold")).pack(pady=5)

        # Video clipping
        clip_frame = tk.Frame(scrollable_frame, bg="#2e3440")
        clip_frame.pack(fill=tk.X, pady=10, padx=5)

        tk.Label(clip_frame, text="Clip Video:",
                 bg="#2e3440", fg="#d8dee9").pack()

        clip_time_frame = tk.Frame(clip_frame, bg="#2e3440")
        clip_time_frame.pack()

        tk.Label(clip_time_frame, text="From:", bg="#2e3440",
                 fg="#d8dee9").grid(row=0, column=0)
        self.clip_start = tk.Entry(clip_time_frame, width=5, bg="#3b4252",
                                   fg="#eceff4")
        self.clip_start.grid(row=0, column=1, padx=2)
        self.clip_start.insert(0, "0")

        tk.Label(clip_time_frame, text="To:", bg="#2e3440",
                 fg="#d8dee9").grid(row=0, column=2, padx=(5, 0))
        self.clip_end = tk.Entry(clip_time_frame, width=5, bg="#3b4252",
                                 fg="#eceff4")
        self.clip_end.grid(row=0, column=3, padx=2)
        self.clip_end.insert(0, "10")

        # Audio option
        self.include_audio_var = tk.BooleanVar(value=True)
        audio_check = tk.Checkbutton(clip_frame, text="Include Audio",
                                     variable=self.include_audio_var,
                                     bg="#2e3440", fg="#d8dee9",
                                     selectcolor="#3b4252",
                                     activebackground="#2e3440",
                                     activeforeground="#d8dee9")
        audio_check.pack(pady=5)

        tk.Button(clip_frame, text="Clip Video",
                  command=self.clip_video,
                  bg="#bf616a", fg="white",
                  font=("Arial", 9, "bold")).pack(pady=5)

        # Extract Audio
        audio_frame = tk.Frame(scrollable_frame, bg="#2e3440")
        audio_frame.pack(fill=tk.X, pady=10, padx=5)

        tk.Label(audio_frame, text="Extract Audio:",
                 bg="#2e3440", fg="#d8dee9").pack()

        audio_format_frame = tk.Frame(audio_frame, bg="#2e3440")
        audio_format_frame.pack(pady=5)

        tk.Label(audio_format_frame, text="Format:",
                 bg="#2e3440", fg="#d8dee9").pack(side=tk.LEFT, padx=5)

        self.audio_format_var = tk.StringVar(value="mp3")
        audio_formats = ["mp3", "wav", "aac", "m4a"]
        audio_dropdown = ttk.Combobox(audio_format_frame,
                                      textvariable=self.audio_format_var,
                                      values=audio_formats,
                                      state="readonly",
                                      width=8)
        audio_dropdown.pack(side=tk.LEFT)

        tk.Button(audio_frame, text="Extract Audio",
                  command=self.extract_audio,
                  bg="#8fbcbb", fg="white",
                  font=("Arial", 9, "bold")).pack(pady=5)

        # Merge Videos
        merge_frame = tk.Frame(scrollable_frame, bg="#2e3440")
        merge_frame.pack(fill=tk.X, pady=10, padx=5)

        tk.Label(merge_frame, text="Merge Videos:",
                 bg="#2e3440", fg="#d8dee9").pack()

        self.merge_count_label = tk.Label(merge_frame,
                                          text="Videos: 0",
                                          bg="#2e3440", fg="#88c0d0",
                                          font=("Arial", 9))
        self.merge_count_label.pack(pady=2)

        merge_btn_frame = tk.Frame(merge_frame, bg="#2e3440")
        merge_btn_frame.pack(pady=5)

        tk.Button(merge_btn_frame, text="Add Videos",
                  command=self.add_videos_to_merge,
                  bg="#5e81ac", fg="white",
                  font=("Arial", 8, "bold"), width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(merge_btn_frame, text="Clear List",
                  command=self.clear_merge_list,
                  bg="#4c566a", fg="white",
                  font=("Arial", 8, "bold"), width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(merge_frame, text="Merge Videos",
                  command=self.merge_videos,
                  bg="#d08770", fg="white",
                  font=("Arial", 9, "bold")).pack(pady=5)

        # Video stats
        tk.Button(scrollable_frame, text="Analyze Video Quality",
                  command=self.analyze_quality,
                  bg="#ebcb8b", fg="black",
                  font=("Arial", 9, "bold")).pack(pady=5, padx=5)

        # FFmpeg path setting
        tk.Button(scrollable_frame, text="Set FFmpeg Path",
                  command=self.set_ffmpeg_path,
                  bg="#4c566a", fg="white",
                  font=("Arial", 8)).pack(pady=5, padx=5)

        # Right panel - Preview
        right_panel = tk.Frame(main_frame, bg="#2e3440")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        preview_label = tk.Label(right_panel, text="Preview",
                                 bg="#2e3440", fg="#d8dee9",
                                 font=("Arial", 12, "bold"))
        preview_label.pack(pady=10)

        self.preview_canvas = tk.Canvas(right_panel, bg="#3b4252",
                                        width=500, height=400)
        self.preview_canvas.pack(padx=10, pady=10)

        # Seekbar controls
        seekbar_frame = tk.Frame(right_panel, bg="#2e3440")
        seekbar_frame.pack(fill=tk.X, padx=10, pady=10)

        # Time display
        self.time_label = tk.Label(seekbar_frame, text="00:00 / 00:00",
                                   bg="#2e3440", fg="#88c0d0",
                                   font=("Arial", 10, "bold"))
        self.time_label.pack()

        # Seekbar
        self.seekbar = ttk.Scale(seekbar_frame, from_=0, to=100,
                                 orient=tk.HORIZONTAL,
                                 command=self.on_seekbar_change)
        self.seekbar.pack(fill=tk.X, pady=5)

        # Playback controls
        controls_frame = tk.Frame(seekbar_frame, bg="#2e3440")
        controls_frame.pack(pady=5)

        tk.Button(controls_frame, text="⏮",
                  command=lambda: self.jump_seconds(-5),
                  bg="#5e81ac", fg="white",
                  font=("Arial", 12, "bold"), width=3).pack(side=tk.LEFT, padx=2)

        tk.Button(controls_frame, text="⏸",
                  command=self.show_current_frame,
                  bg="#5e81ac", fg="white",
                  font=("Arial", 12, "bold"), width=3).pack(side=tk.LEFT, padx=2)

        tk.Button(controls_frame, text="⏭",
                  command=lambda: self.jump_seconds(5),
                  bg="#5e81ac", fg="white",
                  font=("Arial", 12, "bold"), width=3).pack(side=tk.LEFT, padx=2)

        # Status bar
        self.status_label = tk.Label(self.root, text="Ready",
                                     bg="#2e3440", fg="#a3be8c",
                                     anchor=tk.W, padx=10)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                       ("All Files", "*.*")]
        )

        if file_path:
            self.video_path = file_path
            self.file_label.config(text=Path(file_path).name)
            self.load_video_info()
            self.show_first_frame()
            self.status_label.config(text=f"Loaded: {Path(file_path).name}")

    def load_video_info(self):
        if not self.video_path:
            return

        self.video = cv2.VideoCapture(self.video_path)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.total_frames / self.fps if self.fps > 0 else 0

        # Update seekbar range
        self.seekbar.config(to=self.duration)
        self.seekbar.set(0)
        self.update_time_label(0)

        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        info = f"Duration: {self.duration:.2f} sec\n"
        info += f"FPS: {self.fps:.2f}\n"
        info += f"Frames: {self.total_frames}\n"
        info += f"Resolution: {width}x{height}\n"
        info += f"Size: {os.path.getsize(self.video_path) / (1024 * 1024):.2f} MB"

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", info)
        self.info_text.config(state=tk.DISABLED)

    def show_first_frame(self):
        if not self.video:
            return

        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.video.read()

        if ret:
            self.display_frame(frame)

    def display_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # Resize to fit canvas
        img.thumbnail((480, 380), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(250, 200, image=photo)
        self.preview_canvas.image = photo

    def preview_frame(self):
        if not self.video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return

        try:
            second = float(self.second_entry.get())

            if second < 0 or second > self.duration:
                messagebox.showerror("Invalid Time",
                                     f"Time must be between 0 and {self.duration:.2f}")
                return

            self.show_frame_at_time(second)
            self.seekbar.set(second)
            self.status_label.config(text=f"Previewing frame at {second:.2f}s")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")

    def show_frame_at_time(self, second):
        if not self.video_path:
            return

        video = cv2.VideoCapture(self.video_path)
        frame_num = int(second * self.fps)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = video.read()

        if ret:
            self.display_frame(frame)
            self.current_position = second
            self.update_time_label(second)

        video.release()

    def on_seekbar_change(self, value):
        if not self.video_path:
            return

        second = float(value)
        self.show_frame_at_time(second)
        self.second_entry.delete(0, tk.END)
        self.second_entry.insert(0, f"{second:.2f}")

    def update_time_label(self, current_time):
        current_min = int(current_time // 60)
        current_sec = int(current_time % 60)
        total_min = int(self.duration // 60)
        total_sec = int(self.duration % 60)

        time_str = f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}"
        self.time_label.config(text=time_str)

    def jump_seconds(self, seconds):
        if not self.video_path:
            return

        new_position = max(0, min(self.current_position + seconds, self.duration))
        self.seekbar.set(new_position)
        self.show_frame_at_time(new_position)

    def show_current_frame(self):
        if not self.video_path:
            return
        self.show_frame_at_time(self.current_position)

    def extract_frame(self):
        if not self.video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return

        try:
            second = float(self.second_entry.get())

            if second < 0 or second > self.duration:
                messagebox.showerror("Invalid Time",
                                     f"Time must be between 0 and {self.duration:.2f}")
                return

            video = cv2.VideoCapture(self.video_path)
            frame_num = int(second * self.fps)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = video.read()

            if ret:
                output_path = filedialog.asksaveasfilename(
                    defaultextension=".jpg",
                    filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
                )

                if output_path:
                    cv2.imwrite(output_path, frame)
                    self.display_frame(frame)
                    self.status_label.config(text=f"Frame saved: {Path(output_path).name}")
                    messagebox.showinfo("Success", "Frame extracted successfully!")

            video.release()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")

    def create_gif(self):
        if not self.video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return

        try:
            start = float(self.gif_start.get())
            end = float(self.gif_end.get())

            if start >= end or start < 0 or end > self.duration:
                messagebox.showerror("Invalid Range", "Invalid time range!")
                return

            output_path = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF", "*.gif")]
            )

            if not output_path:
                return

            video = cv2.VideoCapture(self.video_path)
            frames = []

            start_frame = int(start * self.fps)
            end_frame = int(end * self.fps)

            self.status_label.config(text="Creating GIF...")
            self.root.update()

            for i in range(start_frame, end_frame, max(1, int(self.fps / 10))):
                video.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = video.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    frames.append(img)

            if frames:
                frames[0].save(output_path, save_all=True,
                               append_images=frames[1:],
                               duration=100, loop=0)
                self.status_label.config(text=f"GIF created: {Path(output_path).name}")
                messagebox.showinfo("Success", "GIF created successfully!")

            video.release()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create GIF: {str(e)}")

    def clip_video(self):
        if not self.video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return

        if not self.ffmpeg_path:
            response = messagebox.askyesno("FFmpeg Not Found",
                                           "FFmpeg is not found automatically.\n\n"
                                           "Do you want to manually select the FFmpeg executable?")
            if response:
                self.set_ffmpeg_path()
            if not self.ffmpeg_path:
                return

        try:
            start_time = float(self.clip_start.get())
            end_time = float(self.clip_end.get())

            if start_time >= end_time or start_time < 0 or end_time > self.duration:
                messagebox.showerror("Invalid Range",
                                     f"Time range must be between 0 and {self.duration:.2f}")
                return

            output_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4", "*.mp4"), ("AVI", "*.avi"), ("MKV", "*.mkv")]
            )

            if not output_path:
                return

            duration = end_time - start_time
            include_audio = self.include_audio_var.get()

            self.status_label.config(text="Clipping video... Please wait")
            self.root.update()

            # Build ffmpeg command
            cmd = [
                self.ffmpeg_path,
                '-i', self.video_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '23'
            ]

            if include_audio:
                cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
            else:
                cmd.extend(['-an'])  # No audio

            cmd.extend(['-y', output_path])

            # Run ffmpeg
            try:
                result = subprocess.run(cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=300)  # 5 minute timeout

                if result.returncode == 0:
                    audio_status = "with audio" if include_audio else "without audio"
                    self.status_label.config(
                        text=f"Video clipped successfully ({audio_status}): {Path(output_path).name}"
                    )
                    messagebox.showinfo("Success",
                                        f"Video clip saved successfully!\n"
                                        f"Duration: {duration:.2f}s\n"
                                        f"Audio: {'Included' if include_audio else 'Removed'}")
                else:
                    error_msg = result.stderr.decode('utf-8', errors='ignore')
                    messagebox.showerror("Error", f"Failed to clip video:\n{error_msg[:300]}")
                    self.status_label.config(text="Error clipping video")

            except subprocess.TimeoutExpired:
                messagebox.showerror("Timeout", "Video clipping took too long and was cancelled.")
                self.status_label.config(text="Clipping timeout")
            except Exception as e:
                messagebox.showerror("Error", f"FFmpeg execution error:\n{str(e)}")
                self.status_label.config(text="Error")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for time!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error")

    def set_ffmpeg_path(self):
        """Manually set FFmpeg path"""
        file_path = filedialog.askopenfilename(
            title="Select FFmpeg Executable",
            filetypes=[("Executable", "*.exe"), ("All Files", "*.*")]
        )

        if file_path and os.path.exists(file_path):
            self.ffmpeg_path = file_path
            messagebox.showinfo("Success", f"FFmpeg path set to:\n{file_path}")
            self.status_label.config(text=f"FFmpeg: {Path(file_path).name}")

    def extract_audio(self):
        if not self.video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return

        if not self.ffmpeg_path:
            response = messagebox.askyesno("FFmpeg Not Found",
                                           "FFmpeg is not found automatically.\n\n"
                                           "Do you want to manually select the FFmpeg executable?")
            if response:
                self.set_ffmpeg_path()
            if not self.ffmpeg_path:
                return

        try:
            audio_format = self.audio_format_var.get()

            output_path = filedialog.asksaveasfilename(
                defaultextension=f".{audio_format}",
                filetypes=[
                    (f"{audio_format.upper()}", f"*.{audio_format}"),
                    ("All Files", "*.*")
                ]
            )

            if not output_path:
                return

            self.status_label.config(text="Extracting audio... Please wait")
            self.root.update()

            # Build ffmpeg command for audio extraction
            cmd = [
                self.ffmpeg_path,
                '-i', self.video_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame' if audio_format == 'mp3' else 'copy',
                '-q:a', '2',  # Quality
                '-y', output_path
            ]

            result = subprocess.run(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    timeout=300)

            if result.returncode == 0:
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                self.status_label.config(
                    text=f"Audio extracted: {Path(output_path).name}"
                )
                messagebox.showinfo("Success",
                                    f"Audio extracted successfully!\n"
                                    f"Format: {audio_format.upper()}\n"
                                    f"Size: {file_size:.2f} MB")
            else:
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                messagebox.showerror("Error", f"Failed to extract audio:\n{error_msg[:300]}")
                self.status_label.config(text="Error extracting audio")

        except subprocess.TimeoutExpired:
            messagebox.showerror("Timeout", "Audio extraction took too long.")
            self.status_label.config(text="Extraction timeout")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error")

    def add_videos_to_merge(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Videos to Merge",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                       ("All Files", "*.*")]
        )

        if file_paths:
            self.merge_video_list.extend(file_paths)
            self.merge_count_label.config(text=f"Videos: {len(self.merge_video_list)}")
            self.status_label.config(text=f"Added {len(file_paths)} video(s) to merge list")

    def clear_merge_list(self):
        self.merge_video_list = []
        self.merge_count_label.config(text="Videos: 0")
        self.status_label.config(text="Merge list cleared")

    def merge_videos(self):
        if len(self.merge_video_list) < 2:
            messagebox.showwarning("Not Enough Videos",
                                   "Please add at least 2 videos to merge!")
            return

        if not self.ffmpeg_path:
            response = messagebox.askyesno("FFmpeg Not Found",
                                           "FFmpeg is not found automatically.\n\n"
                                           "Do you want to manually select the FFmpeg executable?")
            if response:
                self.set_ffmpeg_path()
            if not self.ffmpeg_path:
                return

        try:
            output_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4", "*.mp4"), ("AVI", "*.avi"), ("MKV", "*.mkv")]
            )

            if not output_path:
                return

            self.status_label.config(text=f"Merging {len(self.merge_video_list)} videos... Please wait")
            self.root.update()

            # Create a temporary file list for ffmpeg
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                for video_path in self.merge_video_list:
                    # Use absolute paths and escape special characters
                    abs_path = os.path.abspath(video_path).replace('\\', '/')
                    f.write(f"file '{abs_path}'\n")
                temp_file = f.name

            # Build ffmpeg command for merging
            cmd = [
                self.ffmpeg_path,
                '-f', 'concat',
                '-safe', '0',
                '-i', temp_file,
                '-c', 'copy',
                '-y', output_path
            ]

            result = subprocess.run(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    timeout=600)  # 10 minute timeout

            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass

            if result.returncode == 0:
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                self.status_label.config(
                    text=f"Videos merged: {Path(output_path).name}"
                )
                messagebox.showinfo("Success",
                                    f"Videos merged successfully!\n"
                                    f"Total videos: {len(self.merge_video_list)}\n"
                                    f"Output size: {file_size:.2f} MB")
                self.clear_merge_list()
            else:
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                messagebox.showerror("Error", f"Failed to merge videos:\n{error_msg[:300]}")
                self.status_label.config(text="Error merging videos")

        except subprocess.TimeoutExpired:
            messagebox.showerror("Timeout", "Video merging took too long.")
            self.status_label.config(text="Merging timeout")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error")

    def analyze_quality(self):
        if not self.video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return

        video = cv2.VideoCapture(self.video_path)
        brightness_values = []

        # Sample 10 frames
        for i in range(0, self.total_frames, max(1, self.total_frames // 10)):
            video.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = video.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness_values.append(gray.mean())

        video.release()

        avg_brightness = sum(brightness_values) / len(brightness_values)

        quality_report = f"Quality Analysis:\n\n"
        quality_report += f"Average Brightness: {avg_brightness:.2f}\n"
        quality_report += f"Resolution: {int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))}x"
        quality_report += f"{int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))}\n"
        quality_report += f"Frame Rate: {self.fps:.2f} FPS\n\n"

        if avg_brightness < 80:
            quality_report += "⚠️ Video appears dark\n"
        elif avg_brightness > 180:
            quality_report += "⚠️ Video appears bright\n"
        else:
            quality_report += "✓ Good brightness levels\n"

        if self.fps >= 30:
            quality_report += "✓ Good frame rate"
        else:
            quality_report += "⚠️ Low frame rate"

        messagebox.showinfo("Video Quality Analysis", quality_report)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToolkitApp(root)
    root.mainloop()