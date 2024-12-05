import os




class Videogen:
    def __init__(self, user_input_dic):
        self.user_input_dic = user_input_dic

        
        self.video_topic = self.data.get('video_topic')
        self.video_description = self.data.get('video_description')
        self.audio_engine = self.data.get('audio_engine', 'polly')
        self.theme = self.data.get('theme', 'classic')
        self.video_length = self.data.get('video_length', 60)
        self.selected_language = self.data.get('selected_language', 'Indian English')
        self.selected_narrator = self.data.get('voice_id', 'Kajal')
        self.language_code = None
        self.voice_id = None
        self.topic_name = None
        self.video_data = None
        self.folder_path = None

        #sanity testing of input
        #

    def validate_inputs(self):
        if not self.video_topic or not self.video_description or self.video_description.strip() == "":
            raise ValueError("Topic and Description cannot be empty!")
        self.validate_audio_settings()

    def validate_audio_settings(self):
        if self.audio_engine == 'gtts':
            self.language_code = GTTS_LANGUAGES.get(self.selected_language, "en")
        else:  # audio_engine == 'polly'
            if self.selected_language not in polly_languages:
                raise ValueError("Selected language is not available.")
            if self.selected_narrator not in polly_languages[self.selected_language]['narrators']:
                raise ValueError("Selected narrator is not available for the selected language.")
            self.language_code = polly_languages[self.selected_language]['language_code']
            self.voice_id = self.selected_narrator

    def analyze_prompt_and_fetch_data(self):
        max_retries = 3
        for attempt in range(max_retries):
            analysis_result = analyze_user_prompt(self.video_topic, self.video_description)
            if analysis_result:
                self.topic_name = analysis_result["topic_name"]
                base_data = fetch_data_from_source(analysis_result, self.video_length)
                if base_data:
                    self.video_data = process_fetched_data(self.topic_name, base_data, self.video_length)
                    break
            time.sleep(1)
        if not self.topic_name or not self.video_data:
            raise RuntimeError("Failed to fetch and process data for the video.")

    def save_user_input(self):
        user_input = {
            "video_topic": self.video_topic,
            "video_description": self.video_description,
            "audio_engine": self.audio_engine,
            "theme": self.theme,
            "video_length": self.video_length,
            "selected_language": self.selected_language,
            "voice_id": self.voice_id,
        }
        json_file_path = os.path.join("data", "user_inputs.json")
        append_user_input_to_json(user_input, json_file_path)

    def generate_assets(self):
        self.folder_path = os.path.join("content", self.topic_name)
        os.makedirs(self.folder_path, exist_ok=True)

        for index, slide in enumerate(self.video_data, start=1):
            # Generate Audio
            audio_text = slide.get('narration', '')
            audio_output = (
                google_text_to_speech(audio_text, self.folder_path, index, self.language_code)
                if self.audio_engine == 'gtts'
                else amazon_polly_text_to_speech(audio_text, self.folder_path, index, voice_id=self.voice_id, language_code=self.language_code)
            )
            slide['audio_output'] = audio_output

            # Generate Image
            image_engine = slide['image_engine']
            fallback_image_path = "data/fallback_image.jpg"
            if image_engine == 'bing':
                image_query = slide['image_query']
                image_data = bing_image_downloader(image_query)
                image_path = save_image(image_data, self.folder_path, index) if image_data else fallback_image_path
            else:
                image_prompt = slide['image_prompt']
                image_data = generate_image_with_sd(image_prompt)
                image_path = save_image(image_data, self.folder_path, index) if image_data else fallback_image_path
            slide['image_path'] = image_path

        save_json_file(self.video_data, self.folder_path)

    def create_video(self):
        return create_video(self.video_data, self.folder_path, theme_name=self.theme, video_name=self.topic_name, overall_fps=15)

    def upload_to_s3(self, video_file_path):
        zip_file_path = zip_folder(self.folder_path)
        s3_bucket = "text-to-video-data"
        s3_folder = f"{self.topic_name}/"

        s3_zip_key = f"{s3_folder}{self.topic_name}.zip"
        s3_video_key = f"{s3_folder}{os.path.basename(video_file_path)}"

        s3_zip_url = upload_to_s3(zip_file_path, s3_bucket, s3_zip_key)
        s3_video_url = upload_to_s3(video_file_path, s3_bucket, s3_video_key)

        if not s3_zip_url or not s3_video_url:
            raise RuntimeError("Failed to upload to S3.")

        # Clean up local files
        shutil.rmtree(self.folder_path)
        os.remove(zip_file_path)
        return s3_video_url



    def process(self):
        log.info('validating user input')

        self.validate_inputs()
        self.save_user_input()
        self.analyze_prompt_and_fetch_base_data()
        self.gen_video_template()

        video_file_path = self.generate_video_from_template()

        if self.dev_env == 'False':
            return self.upload_to_s3(video_file_path)
        return video_file_path


ic in python 



# Example usage
def generate_video():
    try:
        request_data = request.json
        videogen = Videogen(request_data, dev_env=os.getenv("DEV_ENV", "False"))
        video_url = videogen.process()
        return jsonify({"video_url": video_url})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500
