from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Dict
import datetime

app = FastAPI()


class LectureInfo(BaseModel):
    days: str
    time: str
    startTime: str
    endTime: str
    location: str
    section: str


class DiscussionInfo(BaseModel):
    days: str
    time: str
    startTime: str
    endTime: str
    location: str
    section: str


class CourseResponse(BaseModel):
    lecture_info: List[LectureInfo]
    discussion_info: Optional[List[DiscussionInfo]]


class UCSDCourseScraper:
    BASE_URL = 'https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm'

    @staticmethod
    def get_headers() -> Dict[str, str]:
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,fr-FR;q=0.7,fr;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=24B9D3FA6D1CBB685981170E336CE668; TS019aef32=01f0fc640d1da84056855354e833d74b71825706ef468e978975ecdfe0c9ec30ce2079ca32dd45f0e3a4e47d258df6e2a70a3af7699c67a2570caf83b044b16b73b30081363501185164267844655e973a2bd4c0c141453f71c05cdf78e5adaf1aae7b98ee; jlinkauthserver=findlay; itscookie=!3U2b2l2erXAHduHBsSSv8z1S6Jjza8zhHe1y8zyvzTTor1NH+NVG2OmqNiBN4a2MfBF216t2rRerazE=; __utmc=57960238; jlinkserver=act; jssoserver=findlay; jlinksessionidx=zd9b546e6955b09917e36aead7dcb2e54; xjlinkloginStudent.Transactional=OK; jlinkappx=/studentAcademicHistory/academichistorystudentdisplay.htm; _ga_1H1H4J36MR=GS1.1.1710223937.10.0.1710223937.0.0.0; _ga_V7PL9NH1RM=GS1.2.1710262840.8.1.1710262879.0.0.0; nmstat=e1a82ff4-8fe2-9a29-fa29-6a49a23b6ce1; _ga_YWRJ9Y5ZE5=GS1.1.1712340807.1.1.1712340959.0.0.0; _ga=GA1.1.1593889766.1691550788; _ga_DQLWSKCKE6=GS1.1.1714347234.3.1.1714347279.0.0.0; _ga_PWJGRGMV0T=GS1.1.1714347146.3.1.1714347292.0.0.0; _ga_0594BCMPWE=GS1.1.1714347292.2.1.1714347317.0.0.0; _uetvid=2d0aa2d00ff511efa12751a9ec2544e9; _ga_8BP9YL1JLD=GS1.1.1715473116.1.1.1715473465.55.0.0; __utma=57960238.1593889766.1691550788.1708020304.1734473723.17; __utmz=57960238.1734473723.17.1.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; TS01111c3f=01f0fc640d3855ee74c6bca91f7f3904787d75c20ab7c4fb19081f91baa1bead42a9c7d827787d1512f9855b012ee30b11c9307ba984e2fb0579cfdd1ea00aa20783f9271e61994b82a8d5d4b9116b6ebda177b886; __utmb=57960238.15.10.1734473723',
            'Host': 'act.ucsd.edu',
            'Origin': 'https://act.ucsd.edu',
            'Referer': 'https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        }

    @staticmethod
    def get_default_form_data() -> Dict[str, str]:
        return {
            'selectedTerm': 'WI25',
            'xsoc_term': '',
            'loggedIn': 'false',
            'tabNum': 'tabs-crs',
            '_selectedSubjects': '1',
            'schedOption1': 'true',
            '_schedOption1': 'on',
            '_schedOption11': 'on',
            '_schedOption12': 'on',
            'schedOption2': 'true',
            'schedOption2': 'on',
            'schedOption4': 'on',
            'schedOption5': 'on',
            'schedOption3': 'on',
            'schedOption7': 'on',
            'schedOption8': 'on',
            'schedOption13': 'on',
            'schedOption10': 'on',
            'schedOption9': 'on',
            'schDay': 'M',
            '_schDay': 'on',
            'schDay': 'T',
            '_schDay': 'on',
            'schDay': 'W',
            '_schDay': 'on',
            'schDay': 'R',
            '_schDay': 'on',
            'schDay': 'F',
            '_schDay': 'on',
            'schDay': 'S',
            '_schDay': 'on',
            'schStartTime': '12:00',
            'schStartAmPm': '0',
            'schEndTime': '12:00',
            'schEndAmPm': '0',
            '_selectedDepartments': '1',
            'schedOption1Dept': 'true',
            '_schedOption1Dept': 'on',
            '_schedOption11Dept': 'on',
            '_schedOption12Dept': 'on',
            'schedOption2Dept': 'true',
            'schedOption2Dept': 'on',
            'schedOption4Dept': 'on',
            'schedOption5Dept': 'on',
            'schedOption3Dept': 'on',
            'schedOption7Dept': 'on',
            'schedOption8Dept': 'on',
            'schedOption13Dept': 'on',
            'schedOption10Dept': 'on',
            'schedOption9Dept': 'on',
            'schDayDept': 'M',
            '_schDayDept': 'on',
            'schDayDept': 'T',
            '_schDayDept': 'on',
            'schDayDept': 'W',
            '_schDayDept': 'on',
            'schDayDept': 'R',
            '_schDayDept': 'on',
            'schDayDept': 'F',
            '_schDayDept': 'on',
            'schDayDept': 'S',
            '_schDayDept': 'on',
            'schStartTimeDept': '12:00',
            'schStartAmPmDept': '0',
            'schEndTimeDept': '12:00',
            'schEndAmPmDept': '0',
            'courses': 'COGS181',
            'sections': '',
            'instructorType': 'begin',
            'instructor': '',
            'titleType': 'contain',
            'title': '',
            '_hideFullSec': 'on',
            '_showPopup': 'on'
        }

    @classmethod
    def create_form_data(cls, course_code: str) -> Dict[str, str]:
        form_data = cls.get_default_form_data()
        form_data['courses'] = course_code
        return form_data

    @classmethod
    async def fetch_course_data(cls, course_code: str) -> List[List[str]]:
        try:
            response = requests.post(
                cls.BASE_URL,
                headers=cls.get_headers(),
                data=cls.create_form_data(course_code)
            )
            response.raise_for_status()
            return cls.parse_response(response.text)
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500, detail="Failed to fetch course data")

    @staticmethod
    def parse_response(html_content: str) -> Dict[str, List[Dict[str, str]]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_='tbrdr')

        if not table:
            raise HTTPException(status_code=404, detail="No courses found")

        lecture_info = []
        discussion_info = []
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if cells and len(cells) > 4 and cells[3].get_text(strip=True) in ["LE", "DI"]:
                course_type = cells[3].get_text(strip=True)
                time_raw = cells[6].get_text(strip=True)
                start_time, end_time = UCSDCourseScraper.parse_time_range(
                    time_raw)
                details = {
                    "days": cells[5].get_text(strip=True),
                    "time": time_raw,
                    "startTime": start_time,
                    "endTime": end_time,
                    "location": cells[7].get_text(strip=True) + " " + cells[8].get_text(strip=True),
                    "section": cells[4].get_text(strip=True)
                }
                if course_type == "LE":
                    lecture_info.append(details)
                elif course_type == "DI":
                    discussion_info.append(details)

        if not lecture_info:
            raise HTTPException(
                status_code=404, detail="No lecture information found")

        return {"lecture_info": lecture_info, "discussion_info": discussion_info}

    @staticmethod
    def parse_time_range(time_raw: str):
        """
        Parse a time string in the format "11:00a-12:20p" into start and end times.

        Args:
            time_raw (str): Raw time string from the table.

        Returns:
            (str, str): Start time and end time in ISO 8601 format (HH:MM:SS).
        """
        try:
            # Ensure there are no extra spaces and split into start and end
            # time_raw = time_raw.replace(" ", "")
            start_raw, end_raw = time_raw.split("-")

            if start_raw[-1] == 'a':
                start_raw = start_raw[:-1] + ' AM'
            else:
                start_raw = start_raw[:-1] + ' PM'
            if end_raw[-1] == 'a':
                end_raw = end_raw[:-1] + ' AM'
            else:
                end_raw = end_raw[:-1] + ' PM'

            # Parse the start and end times
            start_time = datetime.datetime.strptime(
                start_raw, "%I:%M %p").time().strftime("%H:%M")
            end_time = datetime.datetime.strptime(
                end_raw, "%I:%M %p").time().strftime("%H:%M")

            # Return in HH:MM:SS format
            return start_time, end_time
        except ValueError:
            raise HTTPException(
                status_code=500, detail=f"Invalid time format: {time_raw}"
            )


class CourseAPI:
    def __init__(self):
        self.scraper = UCSDCourseScraper()

    async def get_courses(self, course_code: str) -> CourseResponse:
        course_data = await self.scraper.fetch_course_data(course_code)
        return CourseResponse(
            lecture_info=course_data["lecture_info"],
            discussion_info=course_data["discussion_info"]
        )


course_api = CourseAPI()


@app.get("/courses/{course_code}")
async def get_courses(course_code: str):
    return await course_api.get_courses(course_code)
