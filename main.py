import os
from config import ROOT_DATA_DIR, DEFAULT_INPUT
from logger import logger
# from utils import save_as_text_file

logger.info("start!")

class Videogen:
    def __init__(self, user_input_dic):
        self.input = user_input_dic
        self.data_dir = ROOT_DATA_DIR

    def variable_assignment_and_checks(self):
        # assignment
        for key in DEFAULT_INPUT:

            # Get the value from user input or fall back to the default
            value = self.input.get(key, DEFAULT_INPUT[key])
            # Assign it to the instance variable
            self.__dict__[key] = value
            

        #checks  and further modifications
        if self.input.get('video_topic') == '':
            logger.error("feild missing or empty")
            return False
    

    # def generate_slide_content(self):
    #     return get_slide_content_from_source()

    # def generate_slide_blueprint(self):
    #     return get_slide_blueprint_from_llm()

    # def generate_video_from_blueprint(self):
    #     return create_video(self.video_data, self.folder_path, theme_name=self.theme, video_name=self.topic_name, overall_fps=15)
    
    # def save_all_data(self):
    #     save_as_text_file(self.slide_content )


    def run(self):

        logger.info('variable_assignment_and_checks .. ')
        self.variable_assignment_and_checks()

        # log.info('validating user input')
        # self.slide_content = self.generate_slide_content()

        # #get_ audio file

        # #get image
        

        # log.info('validating user input')
        # self.slide_blueprint = self.generate_slide_blueprint()

        # log.info('validating user input')
        # self.output_video_path = self.generate_video_from_blueprint()

        # log.info('validating user input')
        # self.save_all_data()


if __name__ == "__main__":
    topic = input("Enter topic:")
    input = {'video_topic': topic}
    obj = Videogen(input)
    obj.run()