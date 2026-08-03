You are an expert Senior Product Designer, UX Designer, and Full-Stack Software Engineer.

Your task is to design and generate a premium production-ready application called EcoSense AI – Intelligent Forest Soundscape Monitoring Platform.

The application must feel like software developed by Apple, Google, or a modern SaaS company rather than a student project.

Follow every design guideline and functional requirement provided below exactly.

Do not simplify the UI.

Do not skip any screens.

Use reusable components.

Maintain consistency across the entire application.

The application should support future AI integration, Firebase backend integration, and FastAPI APIs.

Focus on creating a scalable and modular architecture.

Generate professional UI components with proper spacing, typography, accessibility, and animations.

PART 1 — PRODUCT VISION & DESIGN FOUNDATION
EcoSense AI
Intelligent Forest Soundscape Monitoring Platform

Version: 1.0

Prepared By: Product Team

1. Product Vision
Vision Statement

EcoSense AI is an intelligent forest monitoring platform that uses Artificial Intelligence to analyze forest soundscapes and provide actionable insights for wildlife conservation and forest protection. The platform transforms raw environmental audio into meaningful information by identifying wildlife species, detecting illegal activities such as chainsaw operations and gunshots, assessing ecosystem health, and notifying forest authorities about critical events.

The long-term vision is to provide an affordable, scalable, and intelligent monitoring solution that supports environmental conservation and assists forest officials in making faster and more informed decisions.

2. Mission

Develop a modern AI-powered platform that continuously analyzes forest audio recordings and delivers accurate wildlife detection, threat identification, biodiversity assessment, and intelligent reporting through a premium and easy-to-use application.

3. Problem Statement

Forest ecosystems are currently monitored using manual surveys, camera traps, and periodic field inspections. These methods are expensive, time-consuming, require significant manpower, and provide only partial coverage of large forest areas. Many illegal activities such as tree cutting and poaching are detected only after damage has occurred.

Although acoustic monitoring devices exist, their recordings often require manual analysis or delayed processing. This limits their usefulness for real-time conservation efforts.

There is a need for an intelligent software platform capable of automatically analyzing forest sounds and presenting the results in an intuitive interface that helps authorities respond quickly to environmental threats.

4. Proposed Solution

EcoSense AI provides an end-to-end software solution for eco-acoustic monitoring.

The application allows authorized users to upload forest audio recordings collected from field devices or acoustic recorders. The system preprocesses the audio using Librosa, converts it into spectrograms, and analyzes it using an Audio Spectrogram Transformer (AST). Based on the AI predictions, the platform identifies wildlife species, detects suspicious sounds such as chainsaws and gunshots, calculates a Forest Health Score, and presents all information through a premium dashboard.

The application also maintains historical records, generates reports, and supports notification mechanisms for important environmental events.

5. Product Goals

The primary goals of EcoSense AI are:

Automate the analysis of forest audio recordings.
Reduce manual effort in wildlife monitoring.
Detect illegal logging and poaching sounds.
Support biodiversity assessment.
Provide an intuitive interface for forest officials and researchers.
Improve decision-making through AI-generated insights.
Maintain historical monitoring records.
Enable scalable deployment for future smart forest initiatives.
6. Target Users
Forest Officers

Use the application to monitor forest conditions, review alerts, and investigate suspicious activities.

Wildlife Researchers

Analyze biodiversity trends, study species distribution, and review historical audio analysis.

Forest Department Administrators

Manage users, monitor overall forest health, review reports, and supervise monitoring operations.

Environmental Organizations

Use monitoring data to support conservation programs and environmental research.

7. Scope of the Project
Included Features
User authentication
Audio upload
Audio playback
Audio preprocessing
Spectrogram generation
AI-based wildlife identification
Threat detection
Forest Health Score calculation
Dashboard visualization
Analysis history
Reports
Notifications
User profile management
Future Scope

The following features are planned for future versions:

Real-time IoT integration
Autonomous acoustic recording devices
Edge AI processing
LoRa communication
Satellite communication
Drone integration
Fire detection
Weather monitoring
Multi-language support
Predictive biodiversity analysis
8. Product Philosophy

EcoSense AI follows five core principles:

Simplicity

The application should remain easy to use even for users with limited technical knowledge.

Intelligence

Artificial Intelligence should reduce manual analysis while improving monitoring efficiency.

Reliability

Every analysis should be repeatable, traceable, and supported by confidence scores.

Accessibility

The interface should support users of different experience levels and be usable on various screen sizes.

Scalability

The architecture should support future expansion with minimal redesign.

9. Core Features

The first version of EcoSense AI will include:

Secure login
Dashboard
Audio upload
AI analysis
Species detection
Threat detection
Forest Health Score
Notifications
History
Reports
Settings
10. User Journey

The user journey follows a simple workflow:

Open the application.
Log in using authorized credentials.
Navigate to the dashboard.
Upload a forest audio recording.
Wait while the system processes the audio.
Review AI-generated analysis results.
View detected species and threats.
Check the Forest Health Score.
Save or export reports.
Review historical monitoring records.
11. Functional Requirements

The system shall:

Authenticate users securely.
Accept WAV and MP3 audio files.
Play uploaded audio.
Preprocess audio using Librosa.
Generate spectrograms.
Run AST for audio classification.
Display species predictions.
Detect chainsaws and gunshots.
Calculate Forest Health Score.
Store results in a database.
Display historical records.
Generate reports.
Send notifications for critical events.
12. Non-Functional Requirements
Fast response time.
Modern and responsive UI.
Secure user authentication.
Easy navigation.
Modular architecture.
High maintainability.
Cross-platform compatibility.
Extensible AI pipeline.
13. Design Principles

The interface should feel:

Professional
Minimal
Modern
Elegant
Calm
Nature-inspired

Avoid clutter.

Present only essential information.

Use whitespace effectively.

Maintain visual consistency.

14. Design Language

Design inspiration:

Apple Human Interface Guidelines
Material Design 3
Linear
Notion
Vercel Dashboard

The interface should communicate trust, clarity, and environmental responsibility.

15. Information Architecture

The application will contain the following primary sections:

Login
Home Dashboard
Upload Audio
Analysis
History
Reports
Notifications
Settings
Profile

Each section should have a clearly defined purpose and minimal navigation depth to improve usability.

16. Development Philosophy

The application will be developed incrementally in independent modules:

Phase 1: User Interface
Phase 2: Audio Processing
Phase 3: AI Integration
Phase 4: Database
Phase 5: Reporting
Phase 6: Final Testing

Each phase should be fully functional before proceeding to the next.

Technology Requirements

The application must be developed using the following technology stack. Do not replace these technologies unless explicitly specified.

Frontend
Streamlit
Python

The frontend should provide a premium, responsive, and interactive user interface with modern dashboards, analytics, audio upload, and visualization capabilities.

Backend
FastAPI

The backend should expose modular REST APIs responsible for AI processing, database communication, authentication, and future integrations.

Artificial Intelligence
PyTorch
Audio Spectrogram Transformer (AST)

The AI module should analyze forest sound recordings and classify:

Bird species
Animal species
Chainsaw sounds
Gunshots
Other environmental sounds

The AI architecture must remain modular to allow future model replacement.

Audio Processing

Use:

Librosa
NumPy
SciPy
SoundFile

Responsibilities include:

Audio loading
Noise reduction
Feature extraction
Spectrogram generation
Audio normalization
Database

During development use:

SQLite

Future production deployment:

Firebase Firestore

All analysis records, user information, predictions, and historical reports should be stored in the database.

Data Visualization

Use:

Plotly
Matplotlib

Display:

Forest Health Trends
Biodiversity Charts
Threat Analysis
Species Frequency
Weekly Reports

Charts should be interactive and responsive.

Authentication

Current Version

Simple Login

Future Version

Firebase Authentication

The architecture should support migration without redesign.

Notifications

Current Version

Dashboard notifications.

Future Version

Firebase Cloud Messaging (FCM).

The notification module should remain independent from the UI.

Reports

Use:

Pandas
ReportLab

Support:

PDF Export
Excel Export
Historical Reports
Version Control

Git

GitHub



1️⃣ Folder Structure

Tell Antigravity exactly how to organize the project.

Example

app/

pages/

components/

services/

database/

models/

utils/

assets/

config/

api/

tests/

requirements.txt
2️⃣ Naming Convention

Example

snake_case

PascalCase

camelCase

Example

upload_audio.py

analysis_service.py

SpeciesCard

ThreatCard

Otherwise Antigravity creates random names.

3️⃣ Component Rules

Instead of

One huge file

Force it to create

Button Component

Card Component

Chart Component

Navigation Component

Upload Component

Alert Component

Species Component

Health Component
4️⃣ State Management

Tell it

Never duplicate state.

Reuse components.

Keep UI and business logic separate.
5️⃣ API Rules

Even before backend

Define endpoints

POST

/upload

POST

/analyze

GET

/history

GET

/report

POST

/login
6️⃣ Database Tables

Even if SQLite

Tell it

Users

AudioFiles

Analysis

Species

Threats

Reports

Notifications

Then later

FastAPI becomes easy.

7️⃣ AI Pipeline

Right now

We only wrote

Upload

↓

Librosa

↓

AST

I want

Audio Upload

↓

Validation

↓

Noise Reduction

↓

Resampling

↓

Feature Extraction

↓

Spectrogram

↓

AST

↓

Confidence Score

↓

Threat Detection

↓

Health Score

↓

Database

↓

Dashboard
8️⃣ Security Rules

Tell it

Validate uploads

Maximum file size

Allowed extensions

Authentication required

No SQL Injection

Escape user input
9️⃣ UX Rules

Instead of saying

Premium

Explain

Every page should contain

Header

Subtitle

Breadcrumb

Action Buttons

Cards

Charts

Tables

Footer
🔟 Future AI

Tell Antigravity

Do not hardcode predictions.

Create reusable AI interfaces.

Future model replacement should require zero UI modification.


3.1 Application Structure

The application shall contain the following screens in the specified order:

Splash Screen
↓
Login
↓
Forgot Password
↓
Dashboard
↓
Upload Audio
↓
Audio Analysis
↓
Forest Health
↓
Alerts
↓
History
↓
Reports
↓
Settings
↓
Profile

Navigation should always be available through a left sidebar (desktop) or bottom navigation (mobile).

3.2 Splash Screen
Purpose

The splash screen introduces the application and establishes the product identity.

Layout
Full-screen background with a subtle forest-themed illustration or gradient.
Application logo centered.
Application name: Eco-Acoustic Health Monitor.
Tagline: Intelligent Forest Soundscape Analysis.
Small loading animation at the bottom.
Behavior
Display for 2–3 seconds.
Automatically navigate to Login if the user is not authenticated.
Navigate to Dashboard if an active session exists.
3.3 Login Screen
Purpose

Allow only authorized users to access the system.

Components
Application logo.
Welcome message.
Email field.
Password field.
Show/Hide password icon.
"Remember Me" checkbox.
Login button.
Forgot Password link.
Version number at the bottom.
Validation
Email format validation.
Password cannot be empty.
Friendly error messages.
Success Flow
Login
↓
Dashboard
3.4 Forgot Password
Components
Email input.
Send Reset Link button.
Success message.
Future Integration

Firebase Authentication.

3.5 Dashboard
Purpose

Provide a complete overview of forest monitoring.

Header
Greeting
Current Date
User Avatar
Notification Bell

Example

Good Morning,
Forest Officer 👋
Statistics Cards

Display four premium cards.

Card 1

Forest Health Score

Example

94%

Healthy

Card 2

Species Detected

28

Card 3

Threats Today

2

Card 4

Total Analyses

156
Quick Actions

Large action cards:

Upload Audio
View Reports
View Alerts
Start Analysis
Recent Activity

Timeline format.

Example

🦜 Indian Peacock
Detected
09:15 AM

⚠ Chainsaw
Detected
10:22 AM

🐦 Asian Koel
Detected
11:04 AM
Charts

Include:

Weekly Forest Health
Species Frequency
Threat Trend

Interactive using Plotly.

3.6 Upload Audio Screen
Purpose

Allow users to upload forest audio.

Components
Drag & Drop upload area.
Upload button.
Supported formats:
WAV
MP3
Maximum file size indicator.
Audio player.
File information.
Display
Filename

forest.wav

Duration

00:18

Sample Rate

22050 Hz

Size

2.4 MB
Buttons
Analyze Audio
Cancel Upload
3.7 AI Processing Screen
Purpose

Display AI processing progress.

Steps
Uploading Audio

↓

Validating File

↓

Reading Audio

↓

Noise Reduction

↓

Generating Spectrogram

↓

Running AST

↓

Generating Prediction

↓

Saving Result

↓

Completed

Each step should have a progress indicator.

3.8 Analysis Result Screen
Layout

Top Card

Species Detected

Indian Peacock

Confidence

96%

Second Card

Threat Detection

Chainsaw

NO

Gunshot

NO

Third Card

Forest Health

94%

Healthy

Fourth Card

Recommendations

Example

No abnormal activity detected.

Continue monitoring.
Visualization

Display:

Waveform
Spectrogram
Confidence Chart
Buttons
Save Report
Export PDF
Analyze Another Audio
3.9 Forest Health Screen

Purpose

Provide a comprehensive overview of ecosystem health.

Display

Overall Score

94%

Biodiversity Index

High

Threat Level

Low

Environmental Status

Healthy

Charts

Weekly Trend
Monthly Trend
Species Growth
3.10 Alerts Screen

Display active alerts.

Card Format

⚠ Chainsaw

Zone A

High Priority

10:32 AM

Severity Levels

Critical
High
Medium
Low

Actions

View Details
Mark as Reviewed
Export Alert
3.11 History Screen

Display all previous analyses.

Columns

Date
Audio Name
Species
Threat
Health Score
Status

Support:

Search
Filter
Sort
Pagination
3.12 Reports Screen

Allow report generation.

Report Types

Daily
Weekly
Monthly
Custom Range

Export Options

PDF
Excel

Include charts and summary statistics.

3.13 Notifications Screen

Display:

AI analysis completed.
Threat detected.
New report generated.
System updates.

Each notification should include:

Icon
Timestamp
Priority
Status
3.14 Settings Screen

Options

Dark Mode
Light Mode
Language
Notification Preferences
About Application
Privacy Policy
Logout
3.15 User Profile

Display

Profile Picture
Name
Email
Role
Organization
Last Login

Buttons

Edit Profile
Change Password
3.16 Navigation Rules

Sidebar must always contain:

🏠 Dashboard

📤 Upload Audio

📊 Analysis

🌳 Forest Health

🔔 Alerts

📜 History

📄 Reports

⚙ Settings

👤 Profile

Current page should always be highlighted.

3.17 User Flow
Launch App

↓

Login

↓

Dashboard

↓

Upload Audio

↓

AI Processing

↓

Analysis Result

↓

Save Report

↓

History

↓

Dashboard
3.18 Error States

Display professional messages for:

Unsupported file.
Upload failed.
AI processing failed.
Database unavailable.
Network disconnected.

Provide retry options.

3.19 Empty States

Examples:

"No reports available yet."

"Upload your first forest audio to begin monitoring."

"No alerts detected today."

Use friendly illustrations and clear call-to-action buttons.

3.20 Success States

After successful analysis:

✅ Analysis Completed Successfully

Species Identified

Forest Health Updated

Report Generated

Provide buttons to view the report or return to the dashboard.


PART 4 — COMPONENT LIBRARY & DESIGN SYSTEM SPECIFICATIONS
4.1 Overview

The application shall use a centralized component library to ensure consistency, maintainability, scalability, and a premium user experience. Every UI element must be reusable and follow a unified design language.

All components should follow Material Design 3 principles while maintaining an Apple-inspired minimal aesthetic.

No page should create its own custom button, card, or input component. Every UI element must be built from reusable components.

4.2 Component Design Principles

Every component should be:

Reusable
Responsive
Accessible
Consistent
Lightweight
Modular
Easy to maintain

Each component should have:

Default State
Hover State
Active State
Disabled State
Loading State
Error State (if applicable)
4.3 Button Component
Purpose

Trigger user actions throughout the application.

Types

Primary Button

Used for:

Login
Upload Audio
Analyze
Save Report

Appearance

Forest Green background
White text
Rounded corners (16px)
Medium elevation
Smooth hover animation

Secondary Button

Used for:

Cancel
Back
View Details

Appearance

White background
Green border
Green text

Danger Button

Used for:

Delete Report
Logout
Clear History

Appearance

Red background
White text

Icon Button

Used for:

Notifications
Settings
Search
Refresh

Icons should use rounded Material Symbols.

4.4 Input Components

All input fields should share the same design.

Text Input

Supports:

Email
Username
Search

Features

Floating label
Placeholder
Validation
Error message
Character limit

Password Field

Includes:

Hide/Show password
Strength indicator
Validation

Search Field

Features

Search icon
Clear button
Auto-complete (future)

Dropdown

Supports:

Species Filter
Date Filter
Forest Zone
Report Type

Date Picker

Supports:

Single Date
Date Range
4.5 Upload Component

Purpose

Upload forest audio recordings.

Features

Drag & Drop
Browse Files
File Validation
Upload Progress
Cancel Upload

Supported Formats

WAV
MP3

Display

File Name
Duration
Sample Rate
File Size
4.6 Audio Player Component

Purpose

Preview uploaded recordings.

Controls

Play
Pause
Stop
Seek Bar
Volume

Display

Current Time
Total Duration
Waveform Preview
4.7 Card Components

Cards are the primary information containers.

Every card should include:

Icon
Title
Content
Optional Action

Statistics Card

Displays:

Forest Health
Species Count
Threat Count
Reports

Species Card

Displays

Species Name
Confidence
Time
Audio Thumbnail
Status

Threat Card

Displays

Threat Type
Priority
Detection Time
Zone
Action Button

Health Score Card

Displays

Overall Score
Biodiversity Rating
Status
Recommendation

Recorder Card (Future)

Displays

Recorder ID
Location
Battery Status
Last Upload
Online Status
4.8 Chart Components

Charts must use Plotly.

Supported Charts

Line Chart
Bar Chart
Pie Chart
Area Chart

Used For

Forest Health Trend
Species Frequency
Threat Trend
Monthly Reports

Charts should support:

Hover Tooltip
Zoom
Export
4.9 Table Component

Supports

Search
Sorting
Filtering
Pagination

Used For

History
Reports
Alerts

Columns should be resizable.

4.10 Notification Component

Categories

Success

Information

Warning

Critical

Each notification includes

Icon
Timestamp
Title
Description
Status

Critical notifications should remain until acknowledged.

4.11 Progress Components

Used during AI processing.

Examples

Uploading Audio

Generating Spectrogram

Running AI Model

Calculating Forest Health

Saving Results

Display

Circular Loader
Linear Progress Bar
Percentage
4.12 Alert Components

Severity Levels

Critical

High

Medium

Low

Colors

Red

Orange

Yellow

Blue

Actions

View

Ignore

Export

4.13 Timeline Component

Used for

Recent Activity
Analysis History
Alerts

Display

Time

↓

Activity

↓

Status

↓

Action

4.14 Report Card

Displays

Report Name
Date
Health Score
Species Count
Threat Count

Actions

View

Download PDF

Download Excel

4.15 AI Result Component

Displays

Species

Confidence

Threat

Health Score

Recommendations

Should be visually separated into individual cards.

4.16 Forest Health Meter

A circular animated gauge displaying:

Overall Health %
Color-coded status
Trend indicator
4.17 Confidence Meter

Displays AI prediction confidence.

Use:

Progress Bar
Circular Ring

Confidence Colors

90–100%

Green

70–89%

Yellow

Below 70%

Red

4.18 Status Chips

Examples

Healthy

Threat

Analyzing

Completed

Processing

Offline

Online

Use pill-shaped chips with subtle colors.

4.19 Empty State Component

When no data exists

Display:

Illustration

Title

Description

Primary Action Button

Example

"No forest recordings available."

4.20 Error State Component

Examples

Unsupported File

AI Model Error

Database Error

Network Error

Each error should include

Icon
Message
Retry Button
4.21 Skeleton Loader

While data loads

Show skeleton versions of

Cards
Tables
Charts
Audio Player

Avoid blank screens.

4.22 Dialog Components

Dialogs required

Delete Confirmation

Logout Confirmation

Export Report

Success Dialog

Warning Dialog

All dialogs should include:

Title
Description
Primary Action
Secondary Action
4.23 Sidebar Component

Desktop Navigation

Dashboard

Upload

Analysis

Forest Health

Alerts

History

Reports

Settings

Profile

The active item should be highlighted with a green accent and subtle background.

4.24 Top Navigation Bar

Contains

Application Logo
Search
Notifications
User Profile
Theme Toggle

Should remain fixed while scrolling.

4.25 Footer

Displays

Application Version

Copyright

Support

Privacy Policy

4.26 Responsive Rules

Desktop

Sidebar Navigation

Tablet

Collapsible Sidebar

Mobile

Bottom Navigation

Components should resize gracefully without breaking layouts.

4.27 Animation Rules

Use subtle animations for:

Button Hover
Card Hover
Sidebar Expansion
Page Transition
Progress Indicators
Success Messages

Avoid excessive animations that distract users.

4.28 Accessibility

Every component must support:

Keyboard Navigation
Screen Readers
High Contrast
Focus Indicators
Minimum Touch Target Size (48x48 px)
4.29 Developer Rules

Every component must:

Be reusable.
Be documented.
Have clear naming.
Follow consistent spacing.
Avoid duplicated code.
Support future extension.
4.30 Component Hierarchy
App
│
├── Layout
│   ├── Sidebar
│   ├── TopBar
│   └── Footer
│
├── Dashboard
│   ├── Statistic Cards
│   ├── Charts
│   ├── Timeline
│   └── Quick Actions
│
├── Upload
│   ├── Upload Widget
│   ├── Audio Player
│   └── Progress
│
├── Analysis
│   ├── Species Card
│   ├── Threat Card
│   ├── Confidence Meter
│   └── Forest Health Card
│
├── Reports
├── History
├── Alerts
└── Settings


PART 5 – AI WORKFLOW & BUSINESS LOGIC
5.1 AI Module Overview
Purpose

The Artificial Intelligence module is the core engine of the Eco-Acoustic Health Monitor. Its primary responsibility is to analyze uploaded forest audio recordings, identify wildlife species, detect potential environmental threats, calculate the Forest Health Score, and provide meaningful recommendations to forest officers.

The AI pipeline should be modular, allowing future replacement or improvement of individual models without affecting the user interface or database.

5.2 AI Workflow Overview

Every uploaded audio file shall follow the same standardized workflow.

User Uploads Audio
        ↓
File Validation
        ↓
Audio Preprocessing
        ↓
Noise Reduction
        ↓
Audio Normalization
        ↓
Feature Extraction
        ↓
Spectrogram Generation
        ↓
AST Model Inference
        ↓
Species Classification
        ↓
Threat Detection
        ↓
Confidence Calculation
        ↓
Forest Health Score
        ↓
Save to Database
        ↓
Dashboard & Reports
5.3 Step 1 – Audio Upload Validation

Before processing, the system shall validate:

File format
File size
Audio duration
Corrupted file detection

Supported Formats

WAV
MP3

Maximum Size

100 MB

Maximum Duration

10 minutes (Prototype)

If validation fails:

Display clear error message.
Stop processing.
5.4 Step 2 – Audio Loading

Use:

Librosa

Responsibilities:

Read audio file.
Convert to mono.
Preserve sampling rate.
Prepare signal for processing.

Display:

Reading Audio...
5.5 Step 3 – Audio Preprocessing

The uploaded audio should be cleaned before AI analysis.

Processing includes:

Noise reduction
Silence removal
Audio normalization
Resampling (e.g., 16 kHz if required by the model)

Purpose:

Improve AI prediction accuracy.

5.6 Step 4 – Feature Extraction

Use Librosa to extract:

Mel Spectrogram
MFCC (if required)
Chroma Features (future)
Spectral Contrast (future)
Zero Crossing Rate (future)

Only the features required by the selected AI model should be passed forward.

5.7 Step 5 – Spectrogram Generation

Convert the processed waveform into a Mel Spectrogram.

The spectrogram should:

Preserve frequency information.
Preserve temporal information.
Be compatible with the AST model input.

Display the generated spectrogram in the Analysis screen.

5.8 Step 6 – AI Model (AST)

Use:

Audio Spectrogram Transformer (AST)

Responsibilities:

Analyze spectrogram.
Classify environmental sounds.
Predict species.
Detect threats.
Generate confidence scores.

The model should remain independent from the UI and backend.

5.9 Step 7 – Species Classification

The AI should identify the most probable wildlife species present in the recording.

For each detected species, display:

Species Name
Scientific Name (Future)
Confidence Score
Detection Timestamp

Example

Indian Peacock

96%

09:24 AM
5.10 Step 8 – Threat Detection

The AI should detect abnormal forest sounds.

Prototype Threats:

Chainsaw
Gunshot
Heavy Vehicle
Human Shouting
Fire Crackling (Future)

Each threat should include:

Confidence
Severity
Timestamp
5.11 Step 9 – Confidence Score

Every prediction should include a confidence percentage.

Confidence Levels

90–100%

High Confidence

70–89%

Medium Confidence

Below 70%

Low Confidence

Low-confidence predictions should be visually distinguished.

5.12 Step 10 – Forest Health Score

The system should calculate an overall Forest Health Score based on:

Species diversity
Number of detected species
Presence of endangered species (future)
Number of threats
Threat severity

Example scoring:

High biodiversity → Higher score
Multiple threats → Lower score
Frequent chainsaw detection → Significant penalty

Display:

Forest Health

94%

Healthy Ecosystem
5.13 Step 11 – Recommendations

Based on the analysis, the AI should generate simple recommendations.

Examples:

No abnormal activity detected. Continue routine monitoring.
Chainsaw activity detected. Inspect the affected zone.
Biodiversity appears low. Increase monitoring frequency.

Recommendations should be concise and easy to understand.

5.14 Step 12 – Database Storage

After analysis, save:

Audio filename
Upload date
Duration
Species detected
Threats detected
Confidence scores
Forest Health Score
Recommendation

The database should support retrieval for reports and historical analysis.

5.15 Step 13 – Dashboard Update

After successful analysis:

Automatically update:

Forest Health Score
Species Count
Threat Count
Recent Activity
Charts
Reports

The user should not need to refresh the page manually.

5.16 AI Processing States

Display progress during processing.

Example:

✔ Upload Completed

✔ Audio Loaded

✔ Preprocessing

✔ Spectrogram Generated

✔ AI Analysis

✔ Species Detected

✔ Threat Detection

✔ Forest Health Calculated

✔ Report Generated
5.17 Error Handling

The AI module should gracefully handle:

Corrupted audio
Unsupported formats
Model loading failure
Prediction timeout
Empty audio
Very noisy recordings

Provide meaningful error messages with retry options.

5.18 Future AI Enhancements

The architecture should support future additions such as:

Multiple AI models
Bird call recognition
Animal call recognition
Fire detection from audio
Rain and weather analysis
Biodiversity index prediction
Real-time streaming analysis
Edge AI deployment
Federated learning
5.19 AI Design Principles

The AI module should follow these principles:

Modular architecture
Explainable predictions
Reusable processing pipeline
High accuracy
Scalable design
Efficient inference
Clear confidence reporting
5.20 AI Workflow Summary
Upload Audio
      ↓
Validate File
      ↓
Read Audio (Librosa)
      ↓
Noise Reduction
      ↓
Normalization
      ↓
Feature Extraction
      ↓
Mel Spectrogram
      ↓
AST Model
      ↓
Species Detection
      ↓
Threat Detection
      ↓
Confidence Calculation
      ↓
Forest Health Score
      ↓
Recommendation
      ↓
Store in Database
      ↓
Update Dashboard
      ↓
Generate Report

PART 6 — BACKEND ARCHITECTURE, DATABASE DESIGN & API SPECIFICATIONS
6.1 Backend Overview

The backend is responsible for connecting the frontend with the Artificial Intelligence module and the database. It manages user authentication, audio processing requests, AI inference, report generation, historical data retrieval, and future integrations such as Firebase and IoT devices.

The backend should be modular, scalable, secure, and easy to maintain.

6.2 Backend Technology Stack

Backend Framework

FastAPI

Programming Language

Python

Database

SQLite (Development)
Firebase Firestore (Future)

AI Framework

PyTorch

Audio Processing

Librosa

API Documentation

Swagger UI (FastAPI)

Version Control

Git
GitHub
6.3 Clean Architecture

The backend should follow a layered architecture.

Presentation Layer (Frontend)
        ↓
REST API Layer (FastAPI)
        ↓
Business Logic Layer
        ↓
AI Processing Layer
        ↓
Database Layer
        ↓
Storage Layer

Each layer must have a single responsibility.

6.4 Folder Structure

The backend should follow the structure below.

backend/

│

├── app/

│   ├── main.py

│   ├── config.py

│

├── api/

│   ├── auth.py

│   ├── upload.py

│   ├── analysis.py

│   ├── report.py

│   ├── history.py

│   ├── notification.py

│

├── services/

│   ├── audio_service.py

│   ├── ai_service.py

│   ├── report_service.py

│   ├── notification_service.py

│

├── database/

│   ├── models.py

│   ├── connection.py

│

├── utils/

│

├── trained_model/

│

├── uploads/

│

└── requirements.txt

Every module should remain independent.

6.5 Database Design

The database should be normalized and designed for future scalability.

Required tables:

Users

Store:

User ID
Name
Email
Password (hashed)
Role
Last Login
AudioFiles

Store:

Audio ID
File Name
File Path
Upload Date
Duration
Sample Rate
Uploaded By
Analysis

Store:

Analysis ID
Audio ID
Processing Date
Forest Health Score
Recommendation
Overall Status
Species

Store:

Species ID
Analysis ID
Species Name
Confidence
Detection Time
Threats

Store:

Threat ID
Analysis ID
Threat Type
Severity
Confidence
Detection Time
Reports

Store:

Report ID
Analysis ID
Generated Date
Report Type
File Path
Notifications

Store:

Notification ID
User ID
Message
Priority
Status
Timestamp
6.6 API Design

The backend should expose RESTful APIs.

Authentication APIs

POST

/api/login

POST

/api/logout

POST

/api/forgot-password
Upload APIs

POST

/api/upload-audio

GET

/api/audio/{id}

DELETE

/api/audio/{id}
AI Analysis APIs

POST

/api/analyze

GET

/api/analysis/{id}

GET

/api/species

GET

/api/threats
Dashboard APIs

GET

/api/dashboard
Report APIs

POST

/api/report/generate

GET

/api/report/{id}
History APIs

GET

/api/history

DELETE

/api/history/{id}
Notification APIs

GET

/api/notifications

PUT

/api/notifications/read
6.7 API Response Format

Every API should return a consistent JSON structure.

Success Response

{
  "success": true,
  "message": "Analysis completed successfully.",
  "data": {}
}

Error Response

{
  "success": false,
  "message": "Invalid audio file.",
  "error_code": "UPLOAD_001"
}
6.8 Authentication Flow
User Login
      ↓
Validate Credentials
      ↓
Generate Session
      ↓
Dashboard Access

Future:

Replace with Firebase Authentication without changing the UI.

6.9 Audio Processing Request Flow
Upload Audio
      ↓
Save File
      ↓
Queue Processing
      ↓
Run AI Pipeline
      ↓
Store Results
      ↓
Return Analysis
6.10 Data Flow
User
      ↓
Frontend
      ↓
FastAPI
      ↓
Librosa
      ↓
AST
      ↓
SQLite
      ↓
Dashboard
6.11 Security Requirements

The backend must:

Validate all uploaded files.
Accept only WAV and MP3 formats.
Hash user passwords.
Prevent SQL injection.
Prevent directory traversal.
Validate all API requests.
Limit upload size.
Log server errors.
6.12 Logging

Maintain logs for:

Login
Upload
Analysis
Errors
Report Generation
Notifications

Logs should include timestamps and severity levels.

6.13 Performance

Target response times:

Login < 2 seconds
Upload < 5 seconds
AI Analysis < 30 seconds (prototype)
Dashboard Load < 3 seconds
6.14 Error Handling

The backend should gracefully handle:

Missing files
Invalid audio
AI failures
Database failures
Network interruptions
Authentication failures

Return descriptive error messages.

6.15 Future Backend Enhancements

The architecture should support:

Firebase Firestore
Cloud Storage
IoT Integration
LoRa Gateways
Edge AI Devices
Push Notifications
GPS-enabled Recorder Locations
Multiple AI Models
6.16 Backend Design Principles

The backend should follow:

Clean Architecture
SOLID Principles
Separation of Concerns
Modular Services
RESTful API Standards
Scalable Design
Maintainable Code
6.17 Backend Workflow Summary
User Request
      ↓
FastAPI Endpoint
      ↓
Validation
      ↓
Business Logic
      ↓
AI Processing (if required)
      ↓
Database Operation
      ↓
API Response
      ↓
Frontend Update

PART 7 — SOFTWARE DEVELOPMENT STANDARDS, PROJECT STRUCTURE & CODING GUIDELINES
7.1 Development Philosophy

The Eco-Acoustic Health Monitor should be developed following modern software engineering principles.

The project must emphasize:

Clean Architecture
Modular Design
Scalability
Readability
Maintainability
Reusability

The application should be easy to extend without modifying existing modules.

7.2 Software Architecture

The project follows a Layered Architecture.

Presentation Layer
        ↓
Business Logic Layer
        ↓
AI Processing Layer
        ↓
Data Access Layer
        ↓
Database

Each layer must remain independent.

7.3 Project Folder Structure
Eco-Acoustic-Health-Monitor/

│
├── frontend/
│
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── assets/
│   ├── styles/
│   ├── utils/
│
├── backend/
│
│   ├── app/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── database/
│   ├── utils/
│
├── ai/
│
│   ├── preprocessing/
│   ├── models/
│   ├── inference/
│   ├── datasets/
│
├── uploads/
│
├── reports/
│
├── tests/
│
├── docs/
│
├── requirements.txt
│
└── README.md
7.4 Coding Standards

The entire project shall follow PEP 8 for Python.

Rules:

Maximum line length: 88–100 characters
Use meaningful variable names
Avoid unused imports
Add comments only where needed
Write readable code instead of clever code
7.5 Naming Conventions
Variables

Use:

snake_case

Example

forest_health_score

audio_file_path

species_count
Functions
snake_case

Example

load_audio()

generate_spectrogram()

predict_species()

calculate_health_score()
Classes

Use:

PascalCase

Example

AudioProcessor

ThreatDetector

SpeciesClassifier
Constants

Use:

UPPER_CASE

Example

MAX_AUDIO_SIZE

SUPPORTED_FORMATS
7.6 File Naming

Examples

audio_service.py

report_service.py

analysis_controller.py

notification_service.py

Never use spaces.

Never use vague names.

7.7 Code Organization

Each file should have one responsibility.

Do NOT place:

Database code
UI code
AI code

inside one file.

Separate them properly.

7.8 Service Layer

Business logic should remain inside Services.

Examples

AudioService

AnalysisService

ReportService

NotificationService

UserService
7.9 Utility Layer

Reusable helper functions belong in Utils.

Examples

Date Formatting

File Validation

Audio Conversion

Common Constants

Logging
7.10 AI Module Standards

The AI folder should contain:

Preprocessing

Inference

Model Loading

Feature Extraction

Prediction

Each step should be independent.

7.11 Database Standards

Every table should have:

Primary Key
Created Date
Updated Date

Relationships must use foreign keys.

Avoid duplicate data.

7.12 Git Workflow

Use meaningful commits.

Examples

Initial project setup

Added dashboard UI

Implemented audio upload

Integrated Librosa preprocessing

Added AST inference

Implemented report generation

Fixed upload validation

Avoid commits like:

update

final

test

changes
7.13 Branch Strategy

Recommended:

main

develop

feature/audio-upload

feature/dashboard

feature/ai-analysis

Merge only after testing.

7.14 Documentation Standards

Every major module should include:

Purpose

Inputs

Outputs

Dependencies

Future Improvements

7.15 Logging Standards

Log:

Login
Upload
Analysis
Errors
Notifications
Report Generation

Each log should include timestamp and severity.

7.16 Error Handling

Every exception should:

Be logged
Show user-friendly messages
Never expose internal details
7.17 Dependency Management

Maintain all packages in:

requirements.txt

Pin versions where appropriate to ensure reproducible environments.

7.18 Code Reusability

Do not duplicate logic.

Create reusable:

Components
Services
Utilities
Database functions
7.19 Performance Guidelines

Optimize:

Audio loading
Database queries
AI inference
Dashboard rendering

Avoid unnecessary processing.

7.20 Security Guidelines

Passwords

Hash before storage

Uploads

Validate extension
Validate MIME type
Validate size

Database

Parameterized queries

Authentication

Session validation
7.21 Testing Strategy

Testing should include:

Unit Testing

Audio processing
AI inference
Database functions

Integration Testing

Upload → AI → Database

UI Testing

Navigation
Upload flow
Dashboard
7.22 Deployment Strategy

Prototype

Local machine

Future

Cloud deployment
Docker
Firebase Hosting
Render/Railway for backend
7.23 Future Scalability

The architecture should support:

Real-time audio streaming
Multiple forests
Multiple organizations
IoT devices
Edge AI
Mobile applications
7.24 Developer Guidelines

Develop features incrementally.

Never leave partially completed modules.

Test before merging.

Keep commits small and meaningful.

Document architectural decisions.

7.25 Quality Assurance

Before every release:

Run tests
Verify UI
Validate AI outputs
Check reports
Review logs
7.26 Success Criteria

The software is considered complete when:

Users can authenticate.
Audio uploads succeed.
AI produces predictions.
Reports are generated.
Dashboard updates automatically.
Data persists in the database.
Errors are handled gracefully.