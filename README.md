## **Overview**
The Gnome is a device designed to empower educators in underserved regions with the tools they need to deliver high-quality education, even without internet connectivity. Powered by advanced AI models and running on a Raspberry Pi, this device enables teachers to access educational resources, generate quizzes, and enhance lesson planning—all offline.

---

## **Features**
- **AI-Driven Assistance**  
   Teachers can interact with the assistant using voice commands to request quizzes, explanations, or lesson planning help.

- **Curated Educational Resources**  
   The device maintains a repository of teacher-requested PDFs that are tailored to their specific classroom needs.

- **Offline Functionality**  
   Entirely independent of internet access, the device is designed to function seamlessly in remote and underserved regions.

- **User-Friendly Interaction**  
   A simple voice-based interface allows teachers to request resources and teaching aids effortlessly.

---

## **Technology Stack**
### **Hardware**
- Raspberry Pi 4 Model B
- Integrated Microphone

### **AI Models**
- **DeepSeek-R1-Distill-Qwen-1.5B**: Handles quiz generation and lesson planning.
- **Cocoro-820M**: Focuses on topic inference and contextual understanding.
- **NLP-Efficient-Companion v3**: Processes natural language queries.

### **Software**
- Python 3
- Ollama Local API
- PDF-to-Text Conversion Tools

### **Storage Management**
- Smart Resource Allocation System for dynamic storage efficiency.

---

## **How It Works**
1. **Requesting Resources**  
   Teachers can request specific educational resources through voice commands.

2. **Content Curation**  
   The assistant creates or retrieves relevant PDFs based on the teacher’s needs, storing them in an organized repository.

3. **Quiz Generation**  
   Using the preloaded resources, the AI generates multiple-choice quizzes to support learning.

4. **Storage Optimization**  
   The system suggests outdated or unused resources for deletion, ensuring the device remains efficient.



## **Credits**  

This project was developed by Dhruv Saini and Sanya Matta. We would like to give special thanks to the teams behind Cocoro-820M and DeepSeek-R1-Distill-Qwen-1.5B for making this project possible.
