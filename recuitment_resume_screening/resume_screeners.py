import ollama
import os
import json
from PyPDF2 import PdfReader
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime

class EnhancedResumeScreener:
    def __init__(self):
        """Initialize the enhanced resume screening system"""
        self.client = ollama.Client()
        self.job_requirements = ""
        self.position_type = ""
        self.results = []
        
        # Define specific criteria for different positions
        self.position_criteria = {
            "BSIT": {
                "required_education": [
                    "Bachelor's degree in Information Technology",
                    "Bachelor's degree in Computer Science", 
                    "Bachelor's degree in Computer Engineering",
                    "Related IT/Technology degree"
                ],
                "required_experience": [
                    "Minimum 2 years teaching experience (preferred)",
                    "Industry experience in IT/Software development",
                    "Training or workshop facilitation experience"
                ],
                "technical_skills": [
                    "Programming languages (Java, Python, C++, etc.)",
                    "Database management (MySQL, PostgreSQL, etc.)",
                    "Web development (HTML, CSS, JavaScript)",
                    "Network administration",
                    "System analysis and design",
                    "Software engineering principles"
                ],
                "certifications": [
                    "Industry certifications (Cisco, Microsoft, Oracle, etc.)",
                    "Teaching certification",
                    "Professional development certificates"
                ]
            },
            "BSHRM": {
                "required_education": [
                    "Bachelor's degree in Hotel and Restaurant Management",
                    "Bachelor's degree in Hospitality Management",
                    "Bachelor's degree in Tourism Management",
                    "Related Hospitality/Business degree"
                ],
                "required_experience": [
                    "Minimum 2 years teaching experience (preferred)",
                    "Hotel/Restaurant industry experience",
                    "Management experience in hospitality sector"
                ],
                "technical_skills": [
                    "Food service management",
                    "Hotel operations management",
                    "Customer service excellence",
                    "Event planning and management",
                    "Financial management in hospitality",
                    "Quality assurance and control"
                ],
                "certifications": [
                    "ServSafe certification",
                    "Hotel management certifications",
                    "Tourism board certifications",
                    "Teaching certification"
                ]
            },
            "BSED_BIOSCI": {
                "required_education": [
                    "Bachelor of Secondary Education major in Biological Science",
                    "Bachelor's degree in Biology with education units",
                    "Master's degree in Biology/Life Sciences (advantage)"
                ],
                "required_experience": [
                    "Teaching experience in secondary education",
                    "Laboratory instruction experience",
                    "Research experience in biological sciences"
                ],
                "technical_skills": [
                    "Laboratory techniques and safety",
                    "Curriculum development for science",
                    "Scientific research methodology",
                    "Educational technology for science",
                    "Assessment and evaluation in science education"
                ],
                "certifications": [
                    "Professional Teaching License",
                    "Laboratory safety certifications",
                    "Continuing professional development units"
                ]
            },
            "BSED_ENGLISH": {
                "required_education": [
                    "Bachelor of Secondary Education major in English",
                    "Bachelor's degree in English/Literature with education units",
                    "Master's degree in English/Literature (advantage)"
                ],
                "required_experience": [
                    "Teaching experience in secondary education",
                    "Writing/editing experience",
                    "Literary analysis and criticism experience"
                ],
                "technical_skills": [
                    "Language proficiency and grammar",
                    "Literature analysis and interpretation",
                    "Writing instruction and assessment",
                    "Reading comprehension strategies",
                    "Educational technology for language arts"
                ],
                "certifications": [
                    "Professional Teaching License",
                    "TESOL/TEFL certification (advantage)",
                    "Writing workshop certifications"
                ]
            },
            "BSED_MATH": {
                "required_education": [
                    "Bachelor of Secondary Education major in Mathematics",
                    "Bachelor's degree in Mathematics with education units",
                    "Master's degree in Mathematics (advantage)"
                ],
                "required_experience": [
                    "Teaching experience in secondary education",
                    "Mathematics tutoring experience",
                    "Curriculum development experience"
                ],
                "technical_skills": [
                    "Advanced mathematical concepts",
                    "Problem-solving methodologies",
                    "Mathematical software proficiency",
                    "Assessment design for mathematics",
                    "Educational technology for math instruction"
                ],
                "certifications": [
                    "Professional Teaching License",
                    "Mathematics education certifications",
                    "Technology integration certificates"
                ]
            }
        }
        
        # Define evaluation criteria
        self.evaluation_criteria = {
            "STRONG_HIRE": {
                "score_range": (85, 100),
                "education": "Exceeds educational requirements with relevant advanced degrees",
                "experience": "5+ years relevant experience with proven track record",
                "skills": "Demonstrates mastery of 80%+ required technical skills",
                "certifications": "Holds multiple relevant certifications",
                "additional": "Shows leadership, innovation, and continuous learning"
            },
            "HIRE": {
                "score_range": (70, 84),
                "education": "Meets educational requirements fully",
                "experience": "3-4 years relevant experience with good performance",
                "skills": "Demonstrates proficiency in 60-79% required technical skills",
                "certifications": "Holds basic required certifications",
                "additional": "Shows potential for growth and development"
            },
            "CONSIDER": {
                "score_range": (50, 69),
                "education": "Meets minimum educational requirements",
                "experience": "1-2 years relevant experience or strong potential",
                "skills": "Demonstrates proficiency in 40-59% required technical skills",
                "certifications": "Some relevant certifications or willing to obtain",
                "additional": "Shows enthusiasm and willingness to learn"
            },
            "REJECT": {
                "score_range": (0, 49),
                "education": "Does not meet minimum educational requirements",
                "experience": "Insufficient relevant experience",
                "skills": "Demonstrates proficiency in <40% required technical skills",
                "certifications": "Lacks essential certifications",
                "additional": "Does not demonstrate basic qualifications for the position"
            }
        }
    
    def set_position_type(self, position):
        """Set the specific teaching position being hired for"""
        position_key = position.upper().replace(" ", "_")
        if position_key in self.position_criteria:
            self.position_type = position_key
            print(f"✅ Set position type: {position}")
            return True
        else:
            available_positions = list(self.position_criteria.keys())
            print(f"❌ Position '{position}' not found. Available positions: {available_positions}")
            return False
    
    def generate_detailed_job_requirements(self, position_key):
        """Generate detailed job requirements for specific position"""
        if position_key not in self.position_criteria:
            return "Position criteria not found"
        
        criteria = self.position_criteria[position_key]
        
        requirements = f"""
POSITION: {position_key.replace('_', ' ')} Teacher

REQUIRED EDUCATION:
{chr(10).join(f"• {req}" for req in criteria['required_education'])}

REQUIRED EXPERIENCE:
{chr(10).join(f"• {req}" for req in criteria['required_experience'])}

REQUIRED TECHNICAL SKILLS:
{chr(10).join(f"• {skill}" for skill in criteria['technical_skills'])}

REQUIRED/PREFERRED CERTIFICATIONS:
{chr(10).join(f"• {cert}" for cert in criteria['certifications'])}

EVALUATION CRITERIA:

STRONG HIRE (85-100 points):
• Education: {self.evaluation_criteria['STRONG_HIRE']['education']}
• Experience: {self.evaluation_criteria['STRONG_HIRE']['experience']}
• Skills: {self.evaluation_criteria['STRONG_HIRE']['skills']}
• Certifications: {self.evaluation_criteria['STRONG_HIRE']['certifications']}
• Additional: {self.evaluation_criteria['STRONG_HIRE']['additional']}

HIRE (70-84 points):
• Education: {self.evaluation_criteria['HIRE']['education']}
• Experience: {self.evaluation_criteria['HIRE']['experience']}
• Skills: {self.evaluation_criteria['HIRE']['skills']}
• Certifications: {self.evaluation_criteria['HIRE']['certifications']}
• Additional: {self.evaluation_criteria['HIRE']['additional']}

CONSIDER (50-69 points):
• Education: {self.evaluation_criteria['CONSIDER']['education']}
• Experience: {self.evaluation_criteria['CONSIDER']['experience']}
• Skills: {self.evaluation_criteria['CONSIDER']['skills']}
• Certifications: {self.evaluation_criteria['CONSIDER']['certifications']}
• Additional: {self.evaluation_criteria['CONSIDER']['additional']}

REJECT (0-49 points):
• Education: {self.evaluation_criteria['REJECT']['education']}
• Experience: {self.evaluation_criteria['REJECT']['experience']}
• Skills: {self.evaluation_criteria['REJECT']['skills']}
• Certifications: {self.evaluation_criteria['REJECT']['certifications']}
• Additional: {self.evaluation_criteria['REJECT']['additional']}
"""
        return requirements
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF files"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {e}")
            return ""
    
    def load_job_requirements(self, position_type):
        """Load job requirements for specific position"""
        print(f"📋 Loading job requirements for: {position_type}")
        
        if not self.set_position_type(position_type):
            return False
        
        self.job_requirements = self.generate_detailed_job_requirements(self.position_type)
        print("✅ Job requirements loaded successfully!")
        print(f"\n📝 **Job Requirements:**\n{self.job_requirements}\n")
        return True
    
    def screen_pdf_resume(self, resume_path, candidate_name):
        """Screen a PDF resume with enhanced criteria"""
        print(f"📄 Screening PDF resume: {candidate_name}")
        
        # Extract text from resume
        resume_text = self.extract_text_from_pdf(resume_path)
        
        if not resume_text:
            return {"name": candidate_name, "score": 0, "recommendation": "Could not read resume", "details": "PDF extraction failed"}
        
        # Create enhanced screening prompt
        prompt = f"""
You are a hiring faculty for educational institutions with expertise in teacher recruitment.

JOB REQUIREMENTS AND EVALUATION CRITERIA:
{self.job_requirements}

CANDIDATE RESUME:
{resume_text}

INSTRUCTIONS:
Please evaluate this candidate systematically using the provided criteria. Your evaluation must include:

1. EDUCATION ANALYSIS (25 points max):
   - Does the candidate meet the educational requirements?
   - Rate their educational background against the criteria
   - Assign points: 0-25

2. EXPERIENCE ANALYSIS (25 points max):
   - Evaluate their teaching and relevant work experience
   - Consider both quantity and quality of experience
   - Assign points: 0-25

3. SKILLS ANALYSIS (25 points max):
   - Check how many required technical skills they demonstrate
   - Assess depth of skill proficiency
   - Assign points: 0-25

4. CERTIFICATIONS ANALYSIS (15 points max):
   - List certifications they possess
   - Evaluate relevance to the position
   - Assign points: 0-15

5. ADDITIONAL QUALIFICATIONS (10 points max):
   - Leadership experience, research, publications, awards
   - Innovation, continuous learning, professional development
   - Assign points: 0-10

6. FINAL RECOMMENDATION:
   Based on total score, provide clear recommendation:
   - STRONG HIRE (85-100): Ready to excel in the position
   - HIRE (70-84): Good candidate, meets requirements well
   - CONSIDER (50-69): Potential candidate with some gaps
   - REJECT (0-49): Does not meet minimum requirements

7. DETAILED JUSTIFICATION:
   - Specific strengths that match job requirements
   - Specific weaknesses or missing qualifications
   - Recommendations for candidate development (if applicable)

Format your response with clear sections and specific point allocations.
"""
        
        try:
            response = self.client.chat(
                model='llava',
                messages=[
                    {'role': 'system', 'content': 'You are an expert educational hiring manager who evaluates teaching candidates systematically using specific criteria.'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            evaluation = response['message']['content']
            
            # Extract score with enhanced parsing
            score = self.extract_score_from_response(evaluation)
            recommendation = self.determine_recommendation(score)
            
            return {
                "name": candidate_name,
                "score": score,
                "recommendation": recommendation,
                "evaluation": evaluation,
                "file_type": "PDF",
                "position": self.position_type
            }
            
        except Exception as e:
            print(f"❌ Error screening resume: {e}")
            return {"name": candidate_name, "score": 0, "recommendation": "REJECT", "evaluation": f"Error: {e}", "file_type": "PDF"}
    
    def screen_image_resume(self, image_path, candidate_name):
        """Screen an image resume with enhanced criteria - FIXED VERSION"""
        print(f"🖼️ Screening image resume: {candidate_name}")
        
        try:
            # Read and process image file
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
            
            # Convert to base64 for Ollama
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = f"""
You are  hiring faculty for educational institutions.

JOB REQUIREMENTS AND EVALUATION CRITERIA:
{self.job_requirements}

Please analyze the resume image and evaluate this candidate using the systematic approach:

1. EDUCATION ANALYSIS (25 points): Educational qualifications vs requirements
2. EXPERIENCE ANALYSIS (25 points): Teaching and relevant work experience
3. SKILLS ANALYSIS (25 points): Required technical skills demonstrated
4. CERTIFICATIONS ANALYSIS (15 points): Relevant certifications held
5. ADDITIONAL QUALIFICATIONS (10 points): Leadership, research, awards, etc.

Provide total score (0-100) and clear recommendation:
- STRONG HIRE (85-100)
- HIRE (70-84)  
- CONSIDER (50-69)
- REJECT (0-49)

Include specific justification for your decision with point breakdown.
"""
            
            # FIXED: Use 'image' instead of 'images' and pass base64 string
            response = self.client.chat(
                model='llava',
                messages=[
                    {'role': 'system', 'content': 'You are an expert educational hiring manager who evaluates teaching candidates systematically.'},
                    {'role': 'user', 'content': prompt, 'images': [image_base64]}
                ]
            )
            
            evaluation = response['message']['content']
            score = self.extract_score_from_response(evaluation)
            recommendation = self.determine_recommendation(score)
            
            return {
                "name": candidate_name,
                "score": score,
                "recommendation": recommendation,
                "evaluation": evaluation,
                "file_type": "Image",
                "position": self.position_type
            }
            
        except Exception as e:
            print(f"❌ Error screening image resume: {e}")
            print(f"Error details: {str(e)}")
            
            # Try alternative approach if first method fails
            try:
                return self.screen_image_resume_alternative(image_path, candidate_name)
            except Exception as e2:
                print(f"❌ Alternative method also failed: {e2}")
                return {"name": candidate_name, "score": 0, "recommendation": "REJECT", "evaluation": f"Error processing image: {e}", "file_type": "Image"}
    
    def screen_image_resume_alternative(self, image_path, candidate_name):
        """Alternative method for screening image resumes"""
        print(f"🔄 Trying alternative method for: {candidate_name}")
        
        try:
            # Alternative approach using direct file path
            prompt = f"""
You are faculty for educational institutions.

JOB REQUIREMENTS AND EVALUATION CRITERIA:
{self.job_requirements}

Please analyze the resume image and evaluate this candidate systematically:

1. EDUCATION ANALYSIS (25 points max)
2. EXPERIENCE ANALYSIS (25 points max)  
3. SKILLS ANALYSIS (25 points max)
4. CERTIFICATIONS ANALYSIS (15 points max)
5. ADDITIONAL QUALIFICATIONS (10 points max)

Provide total score (0-100) and recommendation: STRONG HIRE, HIRE, CONSIDER, or REJECT.
"""
            
            # Read image as bytes
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Use generate method with image
            response = self.client.generate(
                model='llava',
                prompt=prompt,
                images=[image_data]
            )
            
            evaluation = response['response']
            score = self.extract_score_from_response(evaluation)
            recommendation = self.determine_recommendation(score)
            
            return {
                "name": candidate_name,
                "score": score,
                "recommendation": recommendation,
                "evaluation": evaluation,
                "file_type": "Image",
                "position": self.position_type
            }
            
        except Exception as e:
            print(f"❌ Alternative method failed: {e}")
            raise e
    
    def determine_recommendation(self, score):
        """Determine recommendation based on score"""
        if score >= 85:
            return "STRONG HIRE"
        elif score >= 70:
            return "HIRE"
        elif score >= 50:
            return "CONSIDER"
        else:
            return "REJECT"
    
    def extract_score_from_response(self, response_text):
        """Extract numerical score from AI response with enhanced parsing"""
        import re
        
        # Enhanced patterns for score extraction
        patterns = [
            r'total score[:\s]*(\d+)',
            r'final score[:\s]*(\d+)',
            r'overall score[:\s]*(\d+)',
            r'score[:\s]*(\d+)\/100',
            r'score[:\s]*(\d+)\s*points?',
            r'(\d+)\/100',
            r'(\d+)\s*points?\s*total',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response_text.lower())
            if matches:
                # Take the highest score found (likely the total)
                score = max(int(match) for match in matches)
                return min(score, 100)  # Cap at 100
        
        # Fallback: look for recommendation keywords
        response_lower = response_text.lower()
        if 'strong hire' in response_lower:
            return 85
        elif 'hire' in response_lower and 'strong' not in response_lower:
            return 72
        elif 'consider' in response_lower:
            return 55
        elif 'reject' in response_lower:
            return 25
        else:
            return 50  # Default middle score
    
    def process_all_resumes(self, resume_folder, position_type):
        """Process all resumes for specific position"""
        print("🚀 Starting enhanced resume screening process...\n")
        
        # Load job requirements for specific position
        if not self.load_job_requirements(position_type):
            print("❌ Cannot proceed without valid position type")
            return
        
        # Get all resume files
        resume_files = []
        supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        
        for filename in os.listdir(resume_folder):
            file_path = os.path.join(resume_folder, filename)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename.lower())
                if ext in supported_extensions:
                    resume_files.append((file_path, filename))
        
        if not resume_files:
            print(f"❌ No supported resume files found in {resume_folder}")
            print(f"Supported formats: {', '.join(supported_extensions)}")
            return
        
        print(f"📁 Found {len(resume_files)} resume files to process\n")
        
        # Process each resume
        for file_path, filename in resume_files:
            candidate_name = os.path.splitext(filename)[0]
            
            if filename.lower().endswith('.pdf'):
                result = self.screen_pdf_resume(file_path, candidate_name)
            else:  # Image files
                result = self.screen_image_resume(file_path, candidate_name)
            
            self.results.append(result)
            print(f"✅ Completed: {candidate_name} - {result['recommendation']} (Score: {result['score']})\n")
        
        # Generate enhanced report
        self.generate_enhanced_report()
    
    def generate_enhanced_report(self):
        """Generate enhanced screening report with detailed analysis"""
        if not self.results:
            print("❌ No results to report")
            return
        
        # Sort results by score (highest first)
        sorted_results = sorted(self.results, key=lambda x: x['score'], reverse=True)
        
        # Calculate statistics
        scores = [r['score'] for r in self.results]
        recommendations_count = {}
        for result in self.results:
            rec = result['recommendation']
            recommendations_count[rec] = recommendations_count.get(rec, 0) + 1
        
        # Generate enhanced report
        report = f"""
# ENHANCED TEACHER RESUME SCREENING REPORT
**Position:** {self.position_type.replace('_', ' ')} Teacher
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## EXECUTIVE SUMMARY
- **Total Candidates Screened:** {len(self.results)}
- **Average Score:** {sum(scores) / len(scores):.1f}/100
- **Highest Score:** {max(scores)}
- **Lowest Score:** {min(scores)}

## RECOMMENDATION BREAKDOWN
- **🟢 STRONG HIRE (85-100):** {recommendations_count.get('STRONG HIRE', 0)} candidates
- **🔵 HIRE (70-84):** {recommendations_count.get('HIRE', 0)} candidates  
- **🟡 CONSIDER (50-69):** {recommendations_count.get('CONSIDER', 0)} candidates
- **🔴 REJECT (0-49):** {recommendations_count.get('REJECT', 0)} candidates

## POSITION REQUIREMENTS
{self.job_requirements}

## DETAILED CANDIDATE EVALUATIONS

"""
        
        for i, result in enumerate(sorted_results, 1):
            # Determine status emoji and color
            status_info = {
                'STRONG HIRE': ('🟢', 'IMMEDIATE HIRE RECOMMENDED'),
                'HIRE': ('🔵', 'HIRE RECOMMENDED'),
                'CONSIDER': ('🟡', 'CONSIDER WITH RESERVATIONS'),
                'REJECT': ('🔴', 'NOT RECOMMENDED')
            }
            
            emoji, status_text = status_info.get(result['recommendation'], ('⚪', 'UNKNOWN'))
            
            report += f"""
### {i}. {result['name']} - {result['score']}/100
**{emoji} Status:** {status_text}
**File Type:** {result['file_type']}
**Position:** {result.get('position', 'N/A')}

**Detailed Evaluation:**
{result['evaluation']}

{"="*80}
"""
        
        # Add hiring recommendations
        report += f"""

## HIRING RECOMMENDATIONS

### PRIORITY 1 - IMMEDIATE INTERVIEWS
"""
        strong_hires = [r for r in sorted_results if r['recommendation'] == 'STRONG HIRE']
        if strong_hires:
            for candidate in strong_hires:
                report += f"• **{candidate['name']}** - Score: {candidate['score']}/100\n"
        else:
            report += "• No strong hire candidates identified\n"
        
        report += f"""
### PRIORITY 2 - SECOND ROUND INTERVIEWS
"""
        hires = [r for r in sorted_results if r['recommendation'] == 'HIRE']
        if hires:
            for candidate in hires:
                report += f"• **{candidate['name']}** - Score: {candidate['score']}/100\n"
        else:
            report += "• No hire candidates identified\n"
        
        report += f"""
### BACKUP OPTIONS - IF NEEDED
"""
        considers = [r for r in sorted_results if r['recommendation'] == 'CONSIDER']
        if considers:
            for candidate in considers:
                report += f"• **{candidate['name']}** - Score: {candidate['score']}/100 (requires development)\n"
        else:
            report += "• No backup candidates identified\n"
        
        # Save report
        os.makedirs('results', exist_ok=True)
        position_name = self.position_type.replace('_', '-').lower()
        report_path = f"results/enhanced_screening_{position_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📊 **ENHANCED SCREENING COMPLETE!**")
        print(f"📁 Report saved to: {report_path}")
        print(f"\n🏆 **HIRING RECOMMENDATIONS:**")
        print(f"🟢 Strong Hire: {recommendations_count.get('STRONG HIRE', 0)}")
        print(f"🔵 Hire: {recommendations_count.get('HIRE', 0)}")
        print(f"🟡 Consider: {recommendations_count.get('CONSIDER', 0)}")
        print(f"🔴 Reject: {recommendations_count.get('REJECT', 0)}")

def main():
    """Main function with position selection"""
    print("=" * 70)
    print("🎯 ENHANCED TEACHER RESUME SCREENING SYSTEM")
    print("=" * 70)
    
    screener = EnhancedResumeScreener()
    
    # Show available positions
    print("\n📚 AVAILABLE TEACHING POSITIONS:")
    positions = {
        "1": ("BSIT", "Bachelor of Science in Information Technology"),
        "2": ("BSHRM", "BS Hotel Restaurant Management"), 
        "3": ("BSED_BIOSCI", "BSED Major in Biological Science"),
        "4": ("BSED_ENGLISH", "BSED Major in English"),
        "5": ("BSED_MATH", "BSED Major in Mathematics")
    }
    
    for key, (code, description) in positions.items():
        print(f"{key}. {description}")
    
    # Get user selection
    while True:
        choice = input("\n🔢 Select position (1-5): ").strip()
        if choice in positions:
            position_code, position_name = positions[choice]
            print(f"✅ Selected: {position_name}")
            break
        else:
            print("❌ Invalid selection. Please choose 1-5.")
    
    # Configuration
    RESUME_FOLDER = "resumes"
    
    # Check if resume folder exists
    if not os.path.exists(RESUME_FOLDER):
        print(f"❌ Resume folder not found: {RESUME_FOLDER}")
        print("Please create the folder and add resume files")
        return
    
    # Process all resumes for selected position
    screener.process_all_resumes(RESUME_FOLDER, position_code)

if __name__ == "__main__":
    main()