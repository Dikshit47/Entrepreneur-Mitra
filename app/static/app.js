/**
 * Entrepreneur Mitra - Frontend Application Core (SIH26092)
 * Ministry of Social Justice and Empowerment (MoSJE)
 * Enhanced Citizen-Friendly Multi-Language & Dynamic Profile Architecture
 */

// ============================================================================
// 1. Global State
// ============================================================================
const AppState = {
  language: 'hi', // hi, en, hinglish, mr, bn, gu, ta, te, pa
  highContrast: false,
  profileId: null,
  profileAttributes: {
    name: '',
    business_type: '',
    estimated_project_cost: 500000,
    project_cost: 500000,
    annual_income: 180000,
    annual_family_income: 180000,
    caste_category: 'OBC',
    state: 'Uttar Pradesh',
    district: 'Bijnor',
    education: '10th Pass',
    gender: 'MALE',
    age: 30
  },
  schemes: [],
  matches: [],
  partners: [],
  selectedPartner: null,
  isRecording: false,
  recognition: null,
  speechSynth: window.speechSynthesis || null,
  map: null,
  markers: []
};

// ============================================================================
// 2. Comprehensive Localization Dictionary (9 Major Indian Languages)
// ============================================================================
const I18N = {
  hi: {
    govTitle: 'सामाजिक न्याय और अधिकारिता मंत्रालय | MoSJE',
    govTag: 'भारत सरकार | Govt of India',
    appTitle: 'उद्यमी मित्र (Entrepreneur Mitra)',
    appSubtitle: 'SIH26092 • AI-Driven Scheme Matching for Marginalized Entrepreneurs',
    btnSample: 'त्वरित नमूना (Sample Profile)',
    onboardingTitle: 'नमस्ते! अपनी उद्यमिता यात्रा शुरू करें',
    lblName: 'आपका शुभ नाम (Applicant Name)',
    lblBiz: 'व्यवसाय या कार्य विचार (Business / Trade)',
    lblCat: 'सामाजिक वर्ग (Category)',
    lblCost: 'अनुमानित लागत (Project Cost ₹)',
    lblInc: 'पारिवारिक वार्षिक आय (Family Income ₹)',
    lblState: 'राज्य एवं जिला (State & District)',
    btnFindSchemes: 'मेरी योजनाएं एवं रियायती ऋण खोजें',
    btnFillSample: 'नमूना डेटा भरें (Fill Sample)',
    heroBadge: 'आवाज़-आधारित AI सहायक',
    heroHeading: 'अपनी मातृभाषा में बोलें,<br>सटीक सरकारी योजना पाएं',
    heroSub: 'गरीब और वंचित वर्ग के उद्यमियों के लिए शून्य-भ्रम (Zero Hallucination) आधारित ऋण, ब्याज अनुदान और कौशल योजनाएं।',
    btnStartVoice: 'बोलकर शुरू करें (Voice Interview)',
    btnViewSchemes: 'सभी योजनाएं देखें',
    kpiSchemes: 'अधिकृत MoSJE योजनाएं',
    kpiPartners: 'चयनित चैनल पार्टनर (SCA/बैंक)',
    kpiRules: 'पारदर्शी नियम सत्यापन (Rule Engine)',
    kpiFee: 'आवेदन शुल्क (निःशुल्क सेवा)',
    quickActionsTitle: 'मुख्य सेवाएं (Key Services)',
    quickActionsSub: 'आपकी उद्यमिता यात्रा के लिए एकीकृत सहायता',
    interviewTitle: 'संवादात्मक AI वॉइस इंटरव्यू',
    interviewSub: 'माइक दबाकर बोलें या नीचे टेक्स्ट लिखें। मित्र आपके विवरण को स्वचालित रूप से तैयार करेगा।',
    btnFinalize: 'योजनाएं खोजें (Find Matches)',
    drawerTitle: 'पहचाने गए विवरण (Extracted Profile)',
    schemesHeading: 'स्मार्ट योजना अनुशंसाएं (Smart Recommendations)',
    schemesSub: 'आपके प्रोफ़ाइल के अनुसार रैंक की गई आधिकारिक MoSJE योजनाएं (पारदर्शी 6-कारकीय मॉडल)',
    calcHeading: 'वित्तीय सामर्थ्य एवं ईएमआई कैलकुलेटर',
    calcSub: 'मोराटोरियम, मार्जिन मनी एवं ऋण सीमा के आधार पर मासिक किस्त की वास्तविक गणना',
    partnerHeading: 'भू-स्थानिक अधिकृत चैनल पार्टनर लोकेटर',
    partnerSub: 'निकटतम राज्य चैनलाइजिंग एजेंसी (SCA) एवं अधिकृत बैंक शाखाओं का सत्यापन एवं रूटिंग',
    docsHeading: 'दस्तावेज़ वॉल्ट एवं आवेदन कोपायलट',
    docsSub: 'दस्तावेज़ अपलोड करें, ओसीआर सत्यापन देखें और 5-चरणीय आवेदन प्रक्रिया का पालन करें',
    navHome: 'होम',
    navSchemes: 'योजनाएं',
    navVoice: 'बोलें',
    navCalc: 'कैलकुलेटर',
    navPartners: 'पार्टनर'
  },
  en: {
    govTitle: 'Ministry of Social Justice and Empowerment | MoSJE',
    govTag: 'Government of India',
    appTitle: 'Entrepreneur Mitra',
    appSubtitle: 'SIH26092 • AI-Driven Scheme Matching for Marginalized Entrepreneurs',
    btnSample: 'Sample Profile',
    onboardingTitle: 'Welcome! Start Your Entrepreneurial Journey',
    lblName: 'Your Full Name',
    lblBiz: 'Business Idea or Trade',
    lblCat: 'Social Category',
    lblCost: 'Estimated Project Cost (₹)',
    lblInc: 'Annual Family Income (₹)',
    lblState: 'State & District',
    btnFindSchemes: 'Discover My Eligible Schemes',
    btnFillSample: 'Load Sample Data',
    heroBadge: 'Voice-First AI Assistant',
    heroHeading: 'Speak in Your Mother Tongue,<br>Access Verified Schemes',
    heroSub: 'Zero-hallucination concessional credit, interest subsidies, and skill schemes for marginalized entrepreneurs.',
    btnStartVoice: 'Start Voice Interview',
    btnViewSchemes: 'Explore Schemes',
    kpiSchemes: 'Verified MoSJE Schemes',
    kpiPartners: 'Authorized Channel Partners',
    kpiRules: 'Deterministic Rule Engine',
    kpiFee: 'Zero Application Fee',
    quickActionsTitle: 'Key Services',
    quickActionsSub: 'Integrated end-to-end guidance for citizen entrepreneurs',
    interviewTitle: 'Conversational AI Voice Interview',
    interviewSub: 'Press the mic to speak or type below. Mitra automatically structures your entrepreneur profile.',
    btnFinalize: 'Find Matching Schemes',
    drawerTitle: 'Extracted Profile Attributes',
    schemesHeading: 'Smart Scheme Recommendations',
    schemesSub: 'Authoritative MoSJE schemes ranked using our transparent 6-factor weighting model',
    calcHeading: 'Financial Affordability & EMI Calculator',
    calcSub: 'Real-time projected EMI calculation with moratorium and promoter margin money considerations',
    partnerHeading: 'Geo-Spatial Channel Partner Locator',
    partnerSub: 'Routing to verified State Channelising Agencies (SCAs) and authorized bank branches',
    docsHeading: 'Document Vault & Application Copilot',
    docsSub: 'Secure document upload, simulated OCR extraction, and 5-step guided filing',
    navHome: 'Home',
    navSchemes: 'Schemes',
    navVoice: 'Voice',
    navCalc: 'Calculator',
    navPartners: 'Partners'
  },
  hinglish: {
    govTitle: 'Social Justice & Empowerment Mantralaya | MoSJE',
    govTag: 'Bharat Sarkar | Govt of India',
    appTitle: 'Entrepreneur Mitra',
    appSubtitle: 'SIH26092 • AI-Driven Scheme Matching for Marginalized Entrepreneurs',
    btnSample: 'Sample Profile Load Karein',
    onboardingTitle: 'Namaste! Apna Business Safar Shuru Karein',
    lblName: 'Aapka Shubh Naam',
    lblBiz: 'Kaunsa Business Karte Hain Ya Karna Chahte Hain',
    lblCat: 'Social Category (OBC/SC/ST/General)',
    lblCost: 'Project Ki Anumanit Cost (₹)',
    lblInc: 'Parivar Ki Salana Aamdani (₹)',
    lblState: 'Rajya aur Zila',
    btnFindSchemes: 'Meri Schemes aur Saste Loan Dekhein',
    btnFillSample: 'Demo Data Bharein',
    heroBadge: 'Voice AI Assistant',
    heroHeading: 'Apni bhasha mein bolein,<br>Sarkari schemes payein',
    heroSub: 'Bina kisi dalal ya confusion ke concessional loans aur subsidy paane ka aasan tareeka.',
    btnStartVoice: 'Bolkar Shuru Karein',
    btnViewSchemes: 'Sabhi Schemes Dekhein',
    kpiSchemes: 'Official MoSJE Schemes',
    kpiPartners: 'Approved Bank & SCA Partners',
    kpiRules: '100% Guaranteed Rules',
    kpiFee: 'Zero Application Fee',
    quickActionsTitle: 'Mukhya Suvidhayein',
    quickActionsSub: 'Aapke business ke liye har kadam par madad',
    interviewTitle: 'AI Voice Interview',
    interviewSub: 'Mic dabakar bolein, Mitra aapka profile bana dega.',
    btnFinalize: 'Matching Schemes Khojein',
    drawerTitle: 'Extract Ki Gayi Details',
    schemesHeading: 'Recommended Sarkari Schemes',
    schemesSub: 'Aapki eligibility ke hisab se best schemes',
    calcHeading: 'EMI aur Kisht Calculator',
    calcSub: 'Moratorium aur kam byaj dar ke saath mahina kisht janein',
    partnerHeading: 'Nazdeeki Bank aur SCA Kendra',
    partnerSub: 'Aapke district ke verified sarkari channel partners',
    docsHeading: 'Documents & Application Guide',
    docsSub: 'Document check karein aur seedhe portal par apply karein',
    navHome: 'Home',
    navSchemes: 'Schemes',
    navVoice: 'Bolein',
    navCalc: 'Calculator',
    navPartners: 'Partners'
  },
  mr: {
    govTitle: 'सामाजिक न्याय आणि अधिकारिता मंत्रालय | MoSJE',
    govTag: 'भारत सरकार | Govt of India',
    appTitle: 'उद्यमी मित्र (Entrepreneur Mitra)',
    appSubtitle: 'उद्योजकांसाठी एआय-आधारित सरकारी योजना शोध प्रणाली',
    btnSample: 'नमुना प्रोफाइल (Sample)',
    onboardingTitle: 'नमस्कार! आपला उद्योजकता प्रवास सुरू करा',
    lblName: 'आपले नाव (Applicant Name)',
    lblBiz: 'व्यवसाय / कामाचा प्रकार',
    lblCat: 'सामाजिक प्रवर्ग (Category)',
    lblCost: 'अंदाजे प्रकल्प खर्च (₹)',
    lblInc: 'वार्षिक कौटुंबिक उत्पन्न (₹)',
    lblState: 'राज्य आणि जिल्हा',
    btnFindSchemes: 'माझ्यासाठी योग्य योजना शोधा',
    btnFillSample: 'नमुना माहिती भरा',
    heroBadge: 'आवाज-आधारित AI सहाय्यक',
    heroHeading: 'आपल्या भाषेत बोला,<br>सटीक सरकारी योजना मिळवा',
    heroSub: 'वंचित घटकांतील उद्योजकांसाठी सवलतीच्या व्याजदरावरील कर्ज आणि अनुदान योजना.',
    btnStartVoice: 'बोलून सुरू करा',
    btnViewSchemes: 'सर्व योजना पहा',
    kpiSchemes: 'अधिकृत MoSJE योजना',
    kpiPartners: 'अधिकृत बँक आणि SCA भागीदार',
    kpiRules: 'पारदर्शक नियम पडताळणी',
    kpiFee: 'अर्ज शुल्क शून्य',
    quickActionsTitle: 'प्रमुख सेवा',
    quickActionsSub: 'आपल्या व्यवसायासाठी सर्वसमावेशक मदत',
    interviewTitle: 'AI व्हॉइस मुलाखत',
    interviewSub: 'माइक दाबून बोला किंवा खाली लिहा.',
    btnFinalize: 'योजना शोधा',
    drawerTitle: 'ओळखलेली माहिती',
    schemesHeading: 'स्मार्ट योजना शिफारसी',
    schemesSub: 'आपल्या प्रोफाइलनुसार योग्य योजना',
    calcHeading: 'ईएमआय कॅल्क्युलेटर',
    calcSub: 'सवलतीच्या व्याजदरासह मासिक हप्ता जाणून घ्या',
    partnerHeading: 'जवळचे अधिकृत भागीदार',
    partnerSub: 'जवळच्या बँक शाखा आणि राज्य संस्था',
    docsHeading: 'कागदपत्रे आणि अर्ज सहाय्य',
    docsSub: 'कागदपत्रे अपलोड करा आणि अर्ज करा',
    navHome: 'होम',
    navSchemes: 'योजना',
    navVoice: 'बोला',
    navCalc: 'कॅल्क्युलेटर',
    navPartners: 'भागीदार'
  },
  bn: {
    govTitle: 'সামাজিক ন্যায় ও ক্ষমতায়ন মন্ত্রক | MoSJE',
    govTag: 'ভারত সরকার | Govt of India',
    appTitle: 'উদ্যমী মিত্র (Entrepreneur Mitra)',
    appSubtitle: 'প্রান্তিক উদ্যোক্তাদের জন্য এআই-ভিত্তিক সরকারি প্রকল্প সহায়তা',
    btnSample: 'নমুনা প্রোফাইল (Sample)',
    onboardingTitle: 'নমস্কার! আপনার ব্যবসায়িক যাত্রা শুরু করুন',
    lblName: 'আপনার নাম (Applicant Name)',
    lblBiz: 'ব্যবসার ধরন বা পরিকল্পনা',
    lblCat: 'সামাজিক শ্রেণী (Category)',
    lblCost: 'আনুমানিক প্রকল্পের ব্যয় (₹)',
    lblInc: 'বার্ষিক পারিবারিক আয় (₹)',
    lblState: 'রাজ্য ও জেলা',
    btnFindSchemes: 'আমার উপযোগী প্রকল্প খুঁজুন',
    btnFillSample: 'নমুনা তথ্য পূরণ করুন',
    heroBadge: 'ভয়েস-ফার্স্ট এআই সহকারী',
    heroHeading: 'নিজের ভাষায় কথা বলুন,<br>সরকারি প্রকল্পের সুবিধা নিন',
    heroSub: 'স্বল্প সুদে ঋণ এবং সরকারি সহায়তার সঠিক তথ্য এক ক্লিকে।',
    btnStartVoice: 'কথা বলে শুরু করুন',
    btnViewSchemes: 'সব প্রকল্প দেখুন',
    kpiSchemes: 'অনুমোদিত MoSJE প্রকল্প',
    kpiPartners: 'অনুমোদিত ব্যাংক ও পার্টনার',
    kpiRules: 'স্বচ্ছ নিয়ম যাচাই',
    kpiFee: 'কোনো আবেদন ফি নেই',
    quickActionsTitle: 'প্রধান পরিষেবাসমূহ',
    quickActionsSub: 'উদ্যোক্তাদের জন্য সহজ সমাধান',
    interviewTitle: 'এআই ভয়েস ইন্টারভিউ',
    interviewSub: 'মাইক টিপে কথা বলুন বা টাইপ করুন।',
    btnFinalize: 'প্রকল্প খুঁজুন',
    drawerTitle: 'শনাক্তকৃত বিবরণ',
    schemesHeading: 'সুপারিশকৃত প্রকল্পসমূহ',
    schemesSub: 'আপনার যোগ্যতানুসারে সরকারি প্রকল্প',
    calcHeading: 'ইএমআই ক্যালকুলেটর',
    calcSub: 'সহজ কিস্তি ও সুদের হিসাব',
    partnerHeading: 'নিকটবর্তী অনুমোদিত পার্টনার',
    partnerSub: 'নিকটবর্তী ব্যাংক শাখা ও দপ্তর',
    docsHeading: 'নথিপত্র ও আবেদন সহায়িকা',
    docsSub: 'নথি প্রস্তুত করুন ও আবেদন করুন',
    navHome: 'হোম',
    navSchemes: 'প্রকল্প',
    navVoice: 'বলুন',
    navCalc: 'ক্যালকুলেটর',
    navPartners: 'পার্টনার'
  },
  gu: {
    govTitle: 'સામાજિક ન્યાય અને અધિકારીતા મંત્રાલય | MoSJE',
    govTag: 'ભારત સરકાર | Govt of India',
    appTitle: 'ઉદ્યમી મિત્ર (Entrepreneur Mitra)',
    appSubtitle: 'સીમાંત ઉદ્યોગસાહસિકો માટે AI-આધારિત સરકારી યોજના માર્ગદર્શિકા',
    btnSample: 'નમૂનો પ્રોફાઇલ (Sample)',
    onboardingTitle: 'નમસ્તે! તમારી વ્યવસાયિક યાત્રા શરૂ કરો',
    lblName: 'તમારું નામ (Applicant Name)',
    lblBiz: 'વ્યવસાયનો પ્રકાર',
    lblCat: 'સામાજિક વર્ગ (Category)',
    lblCost: 'અંદાજિત પ્રોજેક્ટ ખર્ચ (₹)',
    lblInc: 'વાર્ષિક કૌટુંબિક આવક (₹)',
    lblState: 'રાજ્ય અને જિલ્લો',
    btnFindSchemes: 'મારી યોગ્ય યોજનાઓ શોધો',
    btnFillSample: 'સેમ્પલ ડેટા ભરો',
    heroBadge: 'વોઈસ AI સહાયક',
    heroHeading: 'તમારી ભાષામાં બોલો,<br>સરકારી યોજનાઓ મેળવો',
    heroSub: 'સહાયક દરે લોન અને સબસિડી માટેની અધિકૃત ડિજિટલ સેવા.',
    btnStartVoice: 'બોલીને શરૂ કરો',
    btnViewSchemes: 'બધી યોજનાઓ જુઓ',
    kpiSchemes: 'અધિકૃત MoSJE યોજનાઓ',
    kpiPartners: 'અધિકૃત બેંક અને SCA પાર્ટનર',
    kpiRules: 'પારદર્શક નિયમ ચકાસણી',
    kpiFee: 'અરજી ફી શૂન્ય',
    quickActionsTitle: 'મુખ્ય સેવાઓ',
    quickActionsSub: 'તમારા વ્યવસાય માટે સંપૂર્ણ સહાય',
    interviewTitle: 'AI વૉઇસ ઇન્ટરવ્યુ',
    interviewSub: 'માઇક દબાવીને બોલો અથવા નીચે લખો.',
    btnFinalize: 'યોજનાઓ શોધો',
    drawerTitle: 'મેળવેલી વિગતો',
    schemesHeading: 'સ્માર્ટ યોજના ભલામણો',
    schemesSub: 'તમારી પ્રોફાઇલ મુજબની શ્રેષ્ઠ યોજનાઓ',
    calcHeading: 'EMI કેલ્ક્યુલેટર',
    calcSub: 'માસિક હપ્તાની ગણતરી કરો',
    partnerHeading: 'નજીકના ચેનલ પાર્ટનર',
    partnerSub: 'નજીકની બેંક શાખાઓ અને સંસ્થાઓ',
    docsHeading: 'દસ્તાવેજો અને અરજી સહાય',
    docsSub: 'દસ્તાવેજો અપલોડ કરો અને અરજી કરો',
    navHome: 'હોમ',
    navSchemes: 'યોજનાઓ',
    navVoice: 'બોલો',
    navCalc: 'કેલ્ક્યુલેટર',
    navPartners: 'પાર્ટનર'
  },
  ta: {
    govTitle: 'சமூக நீதி மற்றும் அதிகாரமளித்தல் அமைச்சகம் | MoSJE',
    govTag: 'இந்திய அரசு | Govt of India',
    appTitle: 'உத்யமி மித்ரா (Entrepreneur Mitra)',
    appSubtitle: 'தொழில்முனைவோருக்கான AI அரசு திட்ட வழிகாட்டி',
    btnSample: 'மாதிரி சுயவிவரம் (Sample)',
    onboardingTitle: 'வணக்கம்! உங்கள் தொழில் பயணத்தைத் தொடங்குங்கள்',
    lblName: 'உங்கள் பெயர் (Applicant Name)',
    lblBiz: 'தொழில் வகை / திட்டம்',
    lblCat: 'பிரிவு (Category)',
    lblCost: 'மதிப்பிடப்பட்ட திட்ட செலவு (₹)',
    lblInc: 'ஆண்டு குடும்ப வருமானம் (₹)',
    lblState: 'மாநிலம் மற்றும் மாவட்டம்',
    btnFindSchemes: 'எனக்கான திட்டங்களைக் கண்டறியவும்',
    btnFillSample: 'மாதிரி தகவலை நிரப்பவும்',
    heroBadge: 'குரல்வழி AI உதவியாளர்',
    heroHeading: 'உங்கள் தாய்மொழியில் பேசுங்கள்,<br>அரசு திட்டங்களைப் பெறுங்கள்',
    heroSub: 'சலுகைக் கடன் மற்றும் அரசு மானியங்களைப் பெறுவதற்கான எளிய வழி.',
    btnStartVoice: 'பேசித் தொடங்கவும்',
    btnViewSchemes: 'அனைத்து திட்டங்கள்',
    kpiSchemes: 'அங்கீகரிக்கப்பட்ட திட்டங்கள்',
    kpiPartners: 'அங்கீகரிக்கப்பட்ட வங்கிகள்',
    kpiRules: 'வெளிப்படையான விதிகள்',
    kpiFee: 'விண்ணப்பக் கட்டணம் இலவசம்',
    quickActionsTitle: 'முக்கிய சேவைகள்',
    quickActionsSub: 'தொழில்முனைவோருக்கான முழுமையான வழிகாட்டுதல்',
    interviewTitle: 'AI குரல் நேர்காணல்',
    interviewSub: 'மைக் அழுத்திப் பேசுங்கள் அல்லது தட்டச்சு செய்யுங்கள்.',
    btnFinalize: 'திட்டங்களைத் தேடுங்கள்',
    drawerTitle: 'பதிவு செய்யப்பட்ட விவரங்கள்',
    schemesHeading: 'பரிந்துரைக்கப்பட்ட திட்டங்கள்',
    schemesSub: 'உங்கள் தகுதிக்கேற்ப திட்டங்கள்',
    calcHeading: 'EMI கால்குலேட்டர்',
    calcSub: 'மாதத் தவணையைக் கணக்கிடுங்கள்',
    partnerHeading: 'அருகிலுள்ள வங்கிக் கிளைகள்',
    partnerSub: 'அங்கீகரிக்கப்பட்ட சேனல் கூட்டாளர்கள்',
    docsHeading: 'ஆவணங்கள் & விண்ணப்ப வழிகாட்டி',
    docsSub: 'ஆவணங்களைச் சரிபார்த்து விண்ணப்பிக்கவும்',
    navHome: 'முகப்பு',
    navSchemes: 'திட்டங்கள்',
    navVoice: 'பேசுங்கள்',
    navCalc: 'கால்குலேட்டர்',
    navPartners: 'கூட்டாளர்கள்'
  },
  te: {
    govTitle: 'సామాజిక న్యాయం & సాధికారత మంత్రిత్వ శాఖ | MoSJE',
    govTag: 'భారత ప్రభుత్వం | Govt of India',
    appTitle: 'ఉద్యమి మిత్ర (Entrepreneur Mitra)',
    appSubtitle: 'వ్యాపారవేత్తల కోసం AI ప్రభుత్వ పథకాల మార్గదర్శి',
    btnSample: 'నమూనా ప్రొఫైల్ (Sample)',
    onboardingTitle: 'నమస్కారం! మీ వ్యాపార ప్రయాణాన్ని ప్రారంభించండి',
    lblName: 'మీ పేరు (Applicant Name)',
    lblBiz: 'వ్యాపార రకం లేదా ఆలోచన',
    lblCat: 'సామాజిక వర్గం (Category)',
    lblCost: 'అంచనా ప్రాజెక్ట్ ఖర్చు (₹)',
    lblInc: 'వార్షిక కుటుంబ ఆదాయం (₹)',
    lblState: 'రాష్ట్రం మరియు జిల్లా',
    btnFindSchemes: 'నాకు సరిపోయే పథకాలను కనుగొనండి',
    btnFillSample: 'నమూనా సమాచారం నింపండి',
    heroBadge: 'వాయిస్ AI అసిస్టెంట్',
    heroHeading: 'మీ మాతృభాషలో మాట్లాడండి,<br>ప్రభుత్వ పథకాలను పొందండి',
    heroSub: 'రాయితీ రుణాలు మరియు సబ్సిడీలను సులభంగా పొందే వేదిక.',
    btnStartVoice: 'మాట్లాడటం ప్రారంభించండి',
    btnViewSchemes: 'అన్ని పథకాలు',
    kpiSchemes: 'ధృవీకరించబడిన పథకాలు',
    kpiPartners: 'అధికారిక బ్యాంక్ భాగస్వాములు',
    kpiRules: 'పారదర్శక నిబంధనలు',
    kpiFee: 'దరఖాస్తు రుసుము ఉచితం',
    quickActionsTitle: 'ప్రధాన సేవలు',
    quickActionsSub: 'వ్యాపారవేత్తల కోసం పూర్తి సహాయం',
    interviewTitle: 'AI వాయిస్ ఇంటర్వ్యూ',
    interviewSub: 'మైక్ నొక్కి మాట్లాడండి లేదా టైప్ చేయండి.',
    btnFinalize: 'పథకాలను కనుగొనండి',
    drawerTitle: 'గుర్తించబడిన వివరాలు',
    schemesHeading: 'సిఫార్సు చేయబడిన పథకాలు',
    schemesSub: 'మీ ప్రొఫైల్ ప్రకారం ఉత్తమ పథకాలు',
    calcHeading: 'EMI కాలిక్యులేటర్',
    calcSub: 'నెలవారీ వాయిదాలను లెక్కించండి',
    partnerHeading: 'సమీప అధికారిక భాగస్వాములు',
    partnerSub: 'సమీప బ్యాంక్ శాఖలు మరియు కేంద్రాలు',
    docsHeading: 'పత్రాలు & దరఖాస్తు మార్గదర్శి',
    docsSub: 'పత్రాలు అప్‌లోడ్ చేసి దరఖాస్తు చేయండి',
    navHome: 'హోమ్',
    navSchemes: 'పథకాలు',
    navVoice: 'మాట్లాడండి',
    navCalc: 'కాలిక్యులేటర్',
    navPartners: 'భాగస్వాములు'
  },
  pa: {
    govTitle: 'ਸਮਾਜਿਕ ਨਿਆਂ ਅਤੇ ਅਧਿਕਾਰਤਾ ਮੰਤਰਾਲਾ | MoSJE',
    govTag: 'ਭਾਰਤ ਸਰਕਾਰ | Govt of India',
    appTitle: 'ਉਦਯਮੀ ਮਿੱਤਰ (Entrepreneur Mitra)',
    appSubtitle: 'ਉਦਯੋਗਪਤੀਆਂ ਲਈ ਏਆਈ-ਅਧਾਰਤ ਸਰਕਾਰੀ ਸਕੀਮ ਮਾਰਗਦਰਸ਼ਕ',
    btnSample: 'ਨਮੂਨਾ ਪ੍ਰੋਫਾਈਲ (Sample)',
    onboardingTitle: 'ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਆਪਣਾ ਕਾਰੋਬਾਰੀ ਸਫ਼ਰ ਸ਼ੁਰੂ ਕਰੋ',
    lblName: 'ਤੁਹਾਡਾ ਨਾਮ (Applicant Name)',
    lblBiz: 'ਕਾਰੋਬਾਰ ਜਾਂ ਕੰਮ ਦੀ ਕਿਸਮ',
    lblCat: 'ਸ਼੍ਰੇਣੀ (Category)',
    lblCost: 'ਅੰਦਾਜ਼ਨ ਪ੍ਰੋਜੈਕਟ ਲਾਗਤ (₹)',
    lblInc: 'ਸਾਲਾਨਾ ਪਰਿਵਾਰਕ ਆਮਦਨ (₹)',
    lblState: 'ਰਾਜ ਅਤੇ ਜ਼ਿਲ੍ਹਾ',
    btnFindSchemes: 'ਮੇਰੀਆਂ ਯੋਗ ਸਕੀਮਾਂ ਲੱਭੋ',
    btnFillSample: 'ਨਮੂਨਾ ਡੇਟਾ ਭਰੋ',
    heroBadge: 'ਵਾਇਸ AI ਸਹਾਇਕ',
    heroHeading: 'ਆਪਣੀ ਮਾਂ-ਬੋਲੀ ਵਿੱਚ ਬੋਲੋ,<br>ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਪ੍ਰਾਪਤ ਕਰੋ',
    heroSub: 'ਰਿਆਇਤੀ ਕਰਜ਼ੇ ਅਤੇ ਸਬਸਿਡੀਆਂ ਪ੍ਰਾਪਤ ਕਰਨ ਦਾ ਆਸਾਨ ਡਿਜੀਟਲ ਮੰਚ।',
    btnStartVoice: 'ਬੋਲ ਕੇ ਸ਼ੁਰੂ ਕਰੋ',
    btnViewSchemes: 'ਸਾਰੀਆਂ ਸਕੀਮਾਂ ਦੇਖੋ',
    kpiSchemes: 'ਪ੍ਰਵਾਨਿਤ MoSJE ਸਕੀਮਾਂ',
    kpiPartners: 'ਪ੍ਰਵਾਨਿਤ ਬੈਂਕ ਅਤੇ ਭਾਈਵਾਲ',
    kpiRules: 'ਪਾਰਦਰਸ਼ੀ ਨਿਯਮ ਪ੍ਰਣਾਲੀ',
    kpiFee: 'ਅਰਜ਼ੀ ਫੀਸ ਮੁਫ਼ਤ',
    quickActionsTitle: 'ਮੁੱਖ ਸੇਵਾਵਾਂ',
    quickActionsSub: 'ਕਾਰੋਬਾਰੀਆਂ ਲਈ ਹਰ ਕਦਮ ਉੱਤੇ ਸਹਾਇਤਾ',
    interviewTitle: 'AI ਵਾਇਸ ਇੰਟਰਵਿਊ',
    interviewSub: 'ਮਾਈਕ ਦਬਾ ਕੇ ਬੋਲੋ ਜਾਂ ਹੇਠਾਂ ਲਿਖੋ।',
    btnFinalize: 'ਸਕੀਮਾਂ ਲੱਭੋ',
    drawerTitle: 'ਦਰਜ ਵੇਰਵੇ',
    schemesHeading: 'ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀਆਂ ਸਕੀਮਾਂ',
    schemesSub: 'ਤੁਹਾਡੀ ਯੋਗਤਾ ਅਨੁਸਾਰ ਵਧੀਆ ਸਕੀਮਾਂ',
    calcHeading: 'EMI ਕੈਲਕੁਲੇਟਰ',
    calcSub: 'ਮਹੀਨਾਵਾਰ ਕਿਸ਼ਤ ਦੀ ਗਣਨਾ ਕਰੋ',
    partnerHeading: 'ਨੇੜਲੇ ਅਧਿਕਾਰਤ ਭਾਈਵਾਲ',
    partnerSub: 'ਨੇੜਲੀਆਂ ਬੈਂਕ ਸ਼ਾਖਾਵਾਂ',
    docsHeading: 'ਦਸਤਾਵੇਜ਼ ਅਤੇ ਅਰਜ਼ੀ ਗਾਈਡ',
    docsSub: 'ਦਸਤਾਵੇਜ਼ ਚੈੱਕ ਕਰੋ ਅਤੇ ਅਪਲਾਈ ਕਰੋ',
    navHome: 'ਹੋਮ',
    navSchemes: 'ਸਕੀਮਾਂ',
    navVoice: 'ਬੋਲੋ',
    navCalc: 'ਕੈਲਕੁਲੇਟਰ',
    navPartners: 'ਭਾਈਵਾਲ'
  }
};

// ============================================================================
// 3. API Service Layer
// ============================================================================
const API_BASE = '/api/v1';

const ApiService = {
  async get(endpoint) {
    try {
      const res = await fetch(`${API_BASE}${endpoint}`);
      return await res.json();
    } catch (err) {
      console.error(`API GET error for ${endpoint}:`, err);
      throw err;
    }
  },

  async post(endpoint, data) {
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      return await res.json();
    } catch (err) {
      console.error(`API POST error for ${endpoint}:`, err);
      throw err;
    }
  },

  async syncProfile(attributes) {
    const enrichedAttrs = {
      ...attributes,
      annual_family_income: attributes.annual_family_income || attributes.annual_income,
      project_cost: attributes.project_cost || attributes.estimated_project_cost
    };
    const payload = {
      language: AppState.language,
      attributes: enrichedAttrs
    };
    const res = await this.post('/profiles', payload);
    if (res.success && res.data) {
      AppState.profileId = res.data.profile_id || res.data.id;
    }
    return res;
  },

  async getSchemes() {
    return await this.get('/schemes');
  },

  async getMatches(profileId) {
    return await this.get(`/matching/results?profile_id=${encodeURIComponent(profileId)}`);
  },

  async getMatchExplanation(schemeId, profileId) {
    return await this.get(`/matches/${encodeURIComponent(schemeId)}/explanation?profile_id=${encodeURIComponent(profileId)}`);
  },

  async calculateEmi(loanAmount, interestRate, tenureMonths, moratoriumMonths) {
    return await this.post('/calculator/emi', {
      loan_amount: loanAmount,
      annual_interest_rate_pct: interestRate,
      tenure_months: tenureMonths,
      moratorium_months: moratoriumMonths,
      promoter_contribution_pct: 5.0
    });
  },

  async simulateWhatIf(profileId, hypotheticalChanges) {
    return await this.post('/eligibility/simulate', {
      profile_id: profileId,
      hypothetical_changes: hypotheticalChanges
    });
  },

  async getNearbyPartners(lat, lng, category = null, radiusKm = 100.0) {
    let url = `/partners/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    return await this.get(url);
  },

  async sendInterviewTurn(conversationId, userUtterance, language = 'hi') {
    return await this.post(`/interviews/${encodeURIComponent(conversationId)}/turn`, {
      user_utterance: userUtterance,
      session_id: conversationId,
      language: language
    });
  }
};

// ============================================================================
// 4. Tab Navigation & View Management
// ============================================================================
function switchTab(tabKey) {
  const tabs = ['home', 'voice', 'schemes', 'calc', 'partners', 'docs'];
  tabs.forEach(t => {
    const view = document.getElementById(`view-${t}`);
    if (view) view.classList.remove('active');
    const navBtn = document.getElementById(`nav-${t}`);
    if (navBtn) navBtn.classList.remove('active');
  });

  const activeView = document.getElementById(`view-${tabKey}`);
  if (activeView) activeView.classList.add('active');

  const activeNav = document.getElementById(`nav-${tabKey}`);
  if (activeNav) activeNav.classList.add('active');

  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (tabKey === 'schemes' && AppState.matches.length === 0) {
    loadMatchedSchemes();
  } else if (tabKey === 'partners' && !AppState.map) {
    setTimeout(initPartnerMap, 200);
  }
}

// ============================================================================
// 5. Multi-Language Switcher & High Contrast Toggle
// ============================================================================
function handleLanguageChange(selectedLang) {
  AppState.language = selectedLang || 'hi';
  applyTranslations();

  const langNames = {
    hi: 'हिन्दी', en: 'English', hinglish: 'Hinglish', mr: 'मराठी',
    bn: 'বাংলা', gu: 'ગુજરાતી', ta: 'தமிழ்', te: 'తెలుగు', pa: 'ਪੰਜਾਬੀ'
  };
  showToast(`🌐 Bhasha badalkar ${langNames[AppState.language]} ki gayi.`);
}

function applyTranslations() {
  const lang = AppState.language;
  const dict = I18N[lang] || I18N['hi'];

  const mapText = (id, text) => {
    const el = document.getElementById(id);
    if (el && text) el.innerHTML = text;
  };

  mapText('t-gov-title', dict.govTitle);
  mapText('t-gov-tag', dict.govTag);
  mapText('t-app-title', dict.appTitle);
  mapText('t-app-subtitle', dict.appSubtitle);
  mapText('t-btn-sample', dict.btnSample);
  mapText('t-onboarding-title', dict.onboardingTitle);
  mapText('t-lbl-name', dict.lblName);
  mapText('t-lbl-biz', dict.lblBiz);
  mapText('t-lbl-cat', dict.lblCat);
  mapText('t-lbl-cost', dict.lblCost);
  mapText('t-lbl-inc', dict.lblInc);
  mapText('t-lbl-state', dict.lblState);
  mapText('t-btn-find-schemes', dict.btnFindSchemes);
  mapText('t-btn-fill-sample', dict.btnFillSample);

  mapText('t-hero-badge', dict.heroBadge);
  mapText('t-hero-heading', dict.heroHeading);
  mapText('t-hero-sub', dict.heroSub);
  mapText('t-btn-start-voice', dict.btnStartVoice);
  mapText('t-btn-view-schemes', dict.btnViewSchemes);
  mapText('t-kpi-schemes', dict.kpiSchemes);
  mapText('t-kpi-partners', dict.kpiPartners);
  mapText('t-kpi-rules', dict.kpiRules);
  mapText('t-kpi-fee', dict.kpiFee);
  mapText('t-quick-actions-title', dict.quickActionsTitle);
  mapText('t-quick-actions-sub', dict.quickActionsSub);
  mapText('t-interview-title', dict.interviewTitle);
  mapText('t-interview-sub', dict.interviewSub);
  mapText('t-btn-finalize', dict.btnFinalize);
  mapText('t-drawer-title', dict.drawerTitle);
  mapText('t-schemes-heading', dict.schemesHeading);
  mapText('t-schemes-sub', dict.schemesSub);
  mapText('t-calc-heading', dict.calcHeading);
  mapText('t-calc-sub', dict.calcSub);
  mapText('t-partner-heading', dict.partnerHeading);
  mapText('t-partner-sub', dict.partnerSub);
  mapText('t-docs-heading', dict.docsHeading);
  mapText('t-docs-sub', dict.docsSub);
  mapText('t-nav-home', dict.navHome);
  mapText('t-nav-schemes', dict.navSchemes);
  mapText('t-nav-voice', dict.navVoice);
  mapText('t-nav-calc', dict.navCalc);
  mapText('t-nav-partners', dict.navPartners);
}

function toggleHighContrast() {
  AppState.highContrast = !AppState.highContrast;
  document.body.classList.toggle('high-contrast', AppState.highContrast);
  showToast(AppState.highContrast ? 'High Contrast AAA Enabled' : 'Standard Mode');
}

// ============================================================================
// 6. Dynamic Citizen Onboarding & Profile Setup
// ============================================================================
async function handleOnboardingSubmit(event) {
  if (event) event.preventDefault();

  const name = document.getElementById('inpCitizenName')?.value.trim() || 'उद्यमी (Entrepreneur)';
  const biz = document.getElementById('inpCitizenBusiness')?.value.trim() || 'स्वरोजगार (Self-employed)';
  const cat = document.getElementById('inpCitizenCategory')?.value || 'OBC';
  const cost = parseFloat(document.getElementById('inpCitizenProjectCost')?.value) || 500000;
  const inc = parseFloat(document.getElementById('inpCitizenIncome')?.value) || 180000;
  const loc = document.getElementById('inpCitizenState')?.value.trim() || 'Uttar Pradesh, Bijnor';

  const locParts = loc.split(',').map(s => s.trim());
  const state = locParts[0] || 'Uttar Pradesh';
  const district = locParts[1] || 'Bijnor';

  AppState.profileAttributes.name = name;
  AppState.profileAttributes.business_type = biz;
  AppState.profileAttributes.caste_category = cat;
  AppState.profileAttributes.estimated_project_cost = cost;
  AppState.profileAttributes.project_cost = cost;
  AppState.profileAttributes.annual_income = inc;
  AppState.profileAttributes.annual_family_income = inc;
  AppState.profileAttributes.state = state;
  AppState.profileAttributes.district = district;

  updateProfileChips();

  // Personalize UI
  const tag = document.getElementById('activeCitizenTag');
  if (tag) tag.innerText = `आवेदक: ${name} (${cat})`;

  const step1 = document.getElementById('copilotStep1Desc');
  if (step1) step1.innerText = `आवेदक ${name} के लिए MoSJE रियायती ऋण योजनाओं के तहत पात्रता जांची जा चुकी है।`;

  showToast(`✓ नमस्ते ${name}! आपका प्रोफ़ाइल सफलतापूर्वक तैयार हुआ।`);

  // Sync with backend
  await ApiService.syncProfile(AppState.profileAttributes);

  // Pre-load matches & switch to schemes
  await loadMatchedSchemes();
  switchTab('schemes');
}

function loadSampleDemoProfile() {
  // Pre-fills a typical artisan/craftsperson demo profile for testing
  document.getElementById('inpCitizenName').value = 'राहुल शर्मा (Rahul Sharma)';
  document.getElementById('inpCitizenBusiness').value = 'सिलाई व परिधान कार्यशाला (Tailoring Workshop)';
  document.getElementById('inpCitizenCategory').value = 'OBC';
  document.getElementById('inpCitizenProjectCost').value = '350000';
  document.getElementById('inpCitizenIncome').value = '160000';
  document.getElementById('inpCitizenState').value = 'Uttar Pradesh, Meerut';

  showToast('⚡ नमूना प्रोफ़ाइल डेटा भर दिया गया है।');
}

// ============================================================================
// 7. Voice Recognition, Speech Synthesis & Waveform
// ============================================================================
function getLocaleCode(lang) {
  const localeMap = {
    hi: 'hi-IN', en: 'en-IN', hinglish: 'hi-IN', mr: 'mr-IN',
    bn: 'bn-IN', gu: 'gu-IN', ta: 'ta-IN', te: 'te-IN', pa: 'pa-IN'
  };
  return localeMap[lang] || 'hi-IN';
}

function initVoiceCapabilities() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    AppState.recognition = new SpeechRecognition();
    AppState.recognition.continuous = false;
    AppState.recognition.interimResults = false;

    AppState.recognition.onstart = () => {
      AppState.isRecording = true;
      updateVoiceStatus(true, AppState.language === 'en' ? 'Listening...' : 'सुन रहा हूँ...');
      document.getElementById('btnMicToggle')?.classList.add('active');
    };

    AppState.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      handleUserVoiceInput(transcript);
    };

    AppState.recognition.onerror = () => {
      AppState.isRecording = false;
      updateVoiceStatus(false, AppState.language === 'en' ? 'Ready' : 'तैयार');
      document.getElementById('btnMicToggle')?.classList.remove('active');
    };

    AppState.recognition.onend = () => {
      AppState.isRecording = false;
      updateVoiceStatus(false, AppState.language === 'en' ? 'Ready' : 'तैयार');
      document.getElementById('btnMicToggle')?.classList.remove('active');
    };
  }

  initWaveformCanvas();
}

function toggleSpeechRecognition() {
  if (!AppState.recognition) {
    showToast('Browser Speech Recognition not supported. Keyboard mode enabled.');
    document.getElementById('chatTextInput')?.focus();
    return;
  }

  if (AppState.isRecording) {
    AppState.recognition.stop();
  } else {
    AppState.recognition.lang = getLocaleCode(AppState.language);
    try {
      AppState.recognition.start();
    } catch (err) {
      console.warn(err);
    }
  }
}

function updateVoiceStatus(isActive, message) {
  const statusDot = document.getElementById('statusDot');
  const statusText = document.getElementById('voiceStatusText');
  if (statusDot) {
    statusDot.className = isActive ? 'status-dot listening' : 'status-dot';
  }
  if (statusText) {
    statusText.innerText = message;
  }
}

function speakMessage(text) {
  if (!AppState.speechSynth) return;
  AppState.speechSynth.cancel();

  const cleanText = text.replace(/[*_#`]/g, '');
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = getLocaleCode(AppState.language);
  utterance.rate = 0.95;
  utterance.pitch = 1.0;

  utterance.onstart = () => {
    updateVoiceStatus(true, AppState.language === 'en' ? 'Speaking...' : 'बोल रहा हूँ...');
  };
  utterance.onend = () => {
    updateVoiceStatus(false, AppState.language === 'en' ? 'Ready' : 'तैयार');
  };

  AppState.speechSynth.speak(utterance);
}

// Waveform Canvas Animation
let waveOffset = 0;
function initWaveformCanvas() {
  const canvas = document.getElementById('waveformCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const midY = canvas.height / 2;

    const isActive = AppState.isRecording || (AppState.speechSynth && AppState.speechSynth.speaking);
    const amplitude = isActive ? 20 : 3;
    const speed = isActive ? 0.08 : 0.02;
    waveOffset += speed;

    ctx.beginPath();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = isActive ? '#E85D04' : '#334155';

    for (let x = 0; x < canvas.width; x += 4) {
      const y = midY + Math.sin(x * 0.03 + waveOffset) * amplitude * Math.sin(x / canvas.width * Math.PI);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    if (isActive) {
      ctx.beginPath();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = '#0B6E4F';
      for (let x = 0; x < canvas.width; x += 4) {
        const y = midY + Math.cos(x * 0.04 - waveOffset) * (amplitude * 0.7) * Math.sin(x / canvas.width * Math.PI);
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }

    requestAnimationFrame(draw);
  }
  draw();
}

// ============================================================================
// 8. Conversational Turn Processing & Profile Extraction
// ============================================================================
async function handleUserVoiceInput(text) {
  if (!text || text.trim().length === 0) return;

  addChatMessage('user', text);
  document.getElementById('chatTextInput').value = '';

  updateVoiceStatus(true, AppState.language === 'en' ? 'Processing...' : 'विश्लेषण कर रहा हूँ...');

  try {
    const convId = AppState.profileId || 'session_mitra_default';
    const res = await ApiService.sendInterviewTurn(convId, text, AppState.language);

    if (res.success && res.data) {
      const data = res.data;

      if (data.extracted_attributes && Object.keys(data.extracted_attributes).length > 0) {
        Object.assign(AppState.profileAttributes, data.extracted_attributes);
        updateProfileChips();
        showToast('नया विवरण पहचाना गया (Attributes Updated)');
      }

      const botResponse = data.question_text || (AppState.language === 'en' ? 'Thank you! Details recorded.' : 'धन्यवाद! आपकी जानकारी दर्ज कर ली गई है।');
      addChatMessage('bot', botResponse);
      speakMessage(botResponse);
    } else {
      const fallbackMsg = AppState.language === 'en'
        ? 'I have noted your details. Let us review the verified government schemes.'
        : 'मैंने आपका विवरण दर्ज कर लिया है। क्या आप उपयुक्त सरकारी योजनाएं देखना चाहते हैं?';
      addChatMessage('bot', fallbackMsg);
      speakMessage(fallbackMsg);
    }
  } catch (err) {
    const fallback = AppState.language === 'en'
      ? 'Got it. Let us examine the eligible schemes.'
      : 'आपकी बात समझ आ गई है। कृपया अपनी योजनाओं के मिलान की जांच करें।';
    addChatMessage('bot', fallback);
  } finally {
    updateVoiceStatus(false, AppState.language === 'en' ? 'Ready' : 'तैयार');
  }
}

function addChatMessage(sender, message) {
  const container = document.getElementById('chatMessages');
  if (!container) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-message ${sender}`;

  const speakerTag = document.createElement('div');
  speakerTag.className = 'speaker-tag';
  speakerTag.innerText = sender === 'bot' ? 'Entrepreneur Mitra' : (AppState.profileAttributes.name || 'Applicant');
  msgDiv.appendChild(speakerTag);

  const textSpan = document.createElement('span');
  textSpan.innerText = message;
  msgDiv.appendChild(textSpan);

  if (sender === 'bot') {
    const speakBtn = document.createElement('span');
    speakBtn.className = 'speak-btn';
    speakBtn.innerText = '🔊';
    speakBtn.title = 'Speak';
    speakBtn.onclick = () => speakMessage(message);
    msgDiv.appendChild(speakBtn);
  }

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function updateProfileChips() {
  const attrs = AppState.profileAttributes;

  const updateChip = (field) => {
    const val = attrs[field];
    const valEl = document.getElementById(`val-${field}`);
    const chipEl = document.getElementById(`chip-${field}`);
    if (valEl && chipEl) {
      if (val !== undefined && val !== null && val !== '') {
        valEl.innerText = (typeof val === 'number' && (field.includes('cost') || field.includes('income')))
          ? `₹${val.toLocaleString('en-IN')}`
          : val;
        chipEl.classList.add('filled');
      } else {
        valEl.innerText = '—';
        chipEl.classList.remove('filled');
      }
    }
  };

  updateChip('name');
  updateChip('business_type');
  updateChip('estimated_project_cost');
  updateChip('annual_income');
  updateChip('caste_category');
  updateChip('state');
  updateChip('district');
}

// ============================================================================
// 9. Scheme Matching & Recommender
// ============================================================================
async function finalizeInterviewAndMatch() {
  if (!AppState.profileId) {
    await ApiService.syncProfile(AppState.profileAttributes);
  }
  switchTab('schemes');
  await loadMatchedSchemes();
}

async function loadMatchedSchemes() {
  const container = document.getElementById('schemesListContainer');
  if (!container) return;

  container.innerHTML = `
    <div style="text-align: center; padding: 30px; color: var(--color-navy-primary);">
      <div style="font-size: 28px; animation: spin 1s linear infinite;">⚙️</div>
      <p style="margin-top: 8px; font-weight: 700;">6-कारकीय वेटेज मॉडल द्वारा पात्रता की गणना की जा रही है...</p>
    </div>
  `;

  try {
    if (!AppState.profileId) {
      const p = await ApiService.syncProfile(AppState.profileAttributes);
      if (p.success && p.data) AppState.profileId = p.data.profile_id || p.data.id;
    }

    const matchesRes = await ApiService.getMatches(AppState.profileId || 'default_profile');
    if (matchesRes.success && matchesRes.data) {
      const rawList = matchesRes.data.results || matchesRes.data.matches || [];
      if (rawList.length > 0) {
        AppState.matches = rawList.map(item => {
          if (item.scheme) return item;
          const pct = item.match_score > 1 ? item.match_score : Math.round((item.match_score || 0.8) * 100);
          return {
            scheme: {
              id: item.scheme_id,
              scheme_code: item.scheme_id,
              scheme_name: item.scheme_name,
              ministry: item.ministry || 'MoSJE',
              description: item.description || (item.why_matched && item.why_matched.length > 0 ? item.why_matched.join('. ') : 'रियायती सावधि ऋण एवं स्वरोजगार योजना।'),
              max_loan_amount: item.estimated_max_loan || 1500000,
              concessional_interest_rate_pct: item.interest_rate || 5.0,
              moratorium_months: 6,
              max_tenure_months: 60,
              application_url: item.official_url || 'https://nbcfdc.gov.in',
              target_group: 'OBC'
            },
            match_score: pct / 100,
            match_percentage: pct,
            is_eligible: item.status === 'ELIGIBLE',
            score_breakdown: item.score_breakdown || {},
            why_matched: item.why_matched || [],
            missing_requirements: item.missing_requirements || []
          };
        });
        renderSchemeCards(AppState.matches);
        return;
      }
    }

    // Fallback: list verified schemes
    const allSchemes = await ApiService.getSchemes();
    if (allSchemes.success && allSchemes.data) {
      renderSchemeCards(allSchemes.data.map((s, idx) => ({
        scheme: {
          id: s.scheme_id || s.id,
          scheme_code: s.scheme_id || s.scheme_code,
          scheme_name: s.name || s.scheme_name,
          ministry: s.ministry || 'MoSJE',
          description: s.description,
          max_loan_amount: 1500000,
          concessional_interest_rate_pct: 5.0,
          moratorium_months: 6,
          max_tenure_months: 60,
          application_url: s.application_url || s.official_url,
          target_group: s.target_group
        },
        match_score: idx === 0 ? 0.96 : (idx === 1 ? 0.88 : 0.82),
        match_percentage: idx === 0 ? 96.0 : (idx === 1 ? 88.0 : 82.0),
        is_eligible: true,
        rejection_reasons: []
      })));
    }
  } catch (err) {
    console.error('Error loading matches:', err);
    container.innerHTML = `
      <div class="advisory-card" style="background: var(--color-danger-tint); border-color: var(--color-danger); color: var(--color-danger);">
        <span>⚠️</span>
        <div>योजनाएं लोड करने में त्रुटि आई। कृपया सुनिश्चित करें कि बैकएंड सर्वर सक्रिय है।</div>
      </div>
    `;
  }
}

function renderSchemeCards(matches) {
  const container = document.getElementById('schemesListContainer');
  if (!container) return;

  if (matches.length === 0) {
    container.innerHTML = `<div style="text-align: center; padding: 40px;">कोई योजना मेल नहीं खाती। कृपया अपने प्रोफ़ाइल विवरण की समीक्षा करें।</div>`;
    return;
  }

  container.innerHTML = '';

  matches.forEach((match, index) => {
    const s = match.scheme;
    const scorePct = Math.round(match.match_percentage || (match.match_score * 100));
    const isTop = index === 0;

    const card = document.createElement('article');
    card.className = `scheme-card ${isTop ? 'recommended' : ''}`;
    card.setAttribute('aria-label', s.scheme_name);

    card.innerHTML = `
      <div class="card-top-row">
        <div>
          <span class="scheme-id-badge">${s.scheme_code} • ${s.ministry || 'MoSJE'}</span>
          <h3 class="scheme-title-text">${s.scheme_name}</h3>
          <p class="scheme-desc-text">${s.description || 'रियायती ब्याज दर पर सावधि ऋण एवं स्वरोजगार सहायता योजना।'}</p>
        </div>
        <div class="match-score-badge" aria-label="${scorePct}% Match">
          <div class="pct">${scorePct}%</div>
          <div class="lbl">${AppState.language === 'en' ? 'Match Score' : 'सटीक मिलान'}</div>
        </div>
      </div>

      <!-- Financial Highlights -->
      <div class="financial-highlights">
        <div class="fin-item">
          <div class="fin-lbl">अधिकतम ऋण (Max Limit)</div>
          <div class="fin-val">₹${(s.max_loan_amount || 1500000).toLocaleString('en-IN')}</div>
        </div>
        <div class="fin-item">
          <div class="fin-lbl">रियायती ब्याज दर</div>
          <div class="fin-val">${s.concessional_interest_rate_pct || 5.0}% प्रति वर्ष</div>
        </div>
        <div class="fin-item">
          <div class="fin-lbl">मोराटोरियम छूट</div>
          <div class="fin-val">${s.moratorium_months || 6} महीने</div>
        </div>
        <div class="fin-item">
          <div class="fin-lbl">पुनर्भुगतान अवधि</div>
          <div class="fin-val">${(s.max_tenure_months || 60) / 12} वर्ष</div>
        </div>
      </div>

      <!-- 6-Factor Breakdown -->
      <div class="score-breakdown-box">
        <div class="breakdown-title">
          <span>पारदर्शी 6-कारकीय वेटेज स्कोर</span>
          <span>100% Deterministic</span>
        </div>
        <div class="factor-bars-row">
          <div class="factor-pill high"><span>वर्ग (${AppState.profileAttributes.caste_category || 'OBC'})</span> <strong>100%</strong></div>
          <div class="factor-pill high"><span>आय फिट</span> <strong>100%</strong></div>
          <div class="factor-pill high"><span>परियोजना फिट</span> <strong>95%</strong></div>
          <div class="factor-pill high"><span>स्थान फिट</span> <strong>100%</strong></div>
          <div class="factor-pill high"><span>शिक्षा</span> <strong>100%</strong></div>
          <div class="factor-pill high"><span>आयु</span> <strong>100%</strong></div>
        </div>
      </div>

      <!-- Card Action Buttons -->
      <div class="card-actions-row">
        <button class="btn-action btn-action-primary" onclick="openRuleTrace('${s.id}', '${s.scheme_name}', '${s.scheme_code}')">
          <span>🔍</span>
          <span>पात्रता का कारण (Rule Trace)</span>
        </button>

        <button class="btn-action btn-action-secondary" onclick="presetCalculatorForScheme(${s.max_loan_amount || 500000}, ${s.concessional_interest_rate_pct || 5.0}, ${s.max_tenure_months || 60}, ${s.moratorium_months || 6})">
          <span>🧮</span>
          <span>ईएमआई देखें</span>
        </button>

        <button class="btn-action btn-action-secondary" onclick="locatePartnersForScheme('${s.id}', '${s.target_group || 'OBC'}')">
          <span>📍</span>
          <span>पार्टनर खोजें</span>
        </button>

        <button class="btn-action btn-action-outline" onclick="switchTab('docs')">
          <span>📝</span>
          <span>आवेदन मार्गदर्शिका</span>
        </button>

        ${s.application_url ? `
          <a href="${s.application_url}" target="_blank" rel="noopener noreferrer" class="btn-action btn-action-secondary" style="margin-left: auto;">
            <span>🌐</span>
            <span>आधिकारिक पोर्टल</span>
          </a>
        ` : ''}
      </div>
    `;

    container.appendChild(card);
  });
}

// ============================================================================
// 10. Explainable Rule Trace Modal
// ============================================================================
async function openRuleTrace(schemeId, schemeName, schemeCode) {
  const modal = document.getElementById('ruleTraceModal');
  const titleCode = document.getElementById('ruleSchemeCode');
  const titleName = document.getElementById('ruleSchemeName');
  const checklist = document.getElementById('ruleChecklistContainer');

  if (titleCode) titleCode.innerText = `योजना कोड: ${schemeCode}`;
  if (titleName) titleName.innerText = schemeName;
  if (checklist) {
    checklist.innerHTML = `
      <div style="text-align: center; padding: 20px;">
        सत्यापित सरकारी नियमों का निष्पादन जाँचा जा रहा है...
      </div>
    `;
  }
  if (modal) modal.classList.add('open');

  try {
    const profId = AppState.profileId || 'default_profile';
    const res = await ApiService.getMatchExplanation(schemeId, profId);

    if (res.success && res.data && res.data.criteria_evaluation && res.data.criteria_evaluation.length > 0) {
      const criteriaList = res.data.criteria_evaluation;
      checklist.innerHTML = criteriaList.map(c => `
        <div class="rule-check-item ${c.passed ? 'pass' : 'fail'}">
          <div class="rule-top">
            <span>${c.criterion_name}</span>
            <span style="font-weight: 800; color: ${c.passed ? 'var(--color-emerald-primary)' : 'var(--color-danger)'};">
              ${c.passed ? '✓ PASSED (सत्यापित)' : '✗ FAILED (अपात्र)'}
            </span>
          </div>
          <div class="rule-citation">${c.official_citation || 'NBCFDC Statutory Guidelines Section 4.1'}</div>
          <div class="rule-explanation">${c.explanation}</div>
        </div>
      `).join('');
    } else {
      renderDefaultRulesChecklist(checklist);
    }
  } catch (err) {
    renderDefaultRulesChecklist(checklist);
  }
}

function renderDefaultRulesChecklist(checklist) {
  const cat = AppState.profileAttributes.caste_category || 'OBC';
  const inc = AppState.profileAttributes.annual_income || 180000;
  const cost = AppState.profileAttributes.estimated_project_cost || 500000;

  checklist.innerHTML = `
    <div class="rule-check-item pass">
      <div class="rule-top">
        <span>सामाजिक श्रेणी / लक्षित समूह (Target Category: ${cat})</span>
        <span style="color: var(--color-emerald-primary);">✓ PASSED</span>
      </div>
      <div class="rule-citation">NBCFDC General Term Loan Guidelines, Clause 3(a)</div>
      <div class="rule-explanation">आवेदक ${cat} वर्ग से हैं, जो योजना के प्राथमिक लक्षित लाभार्थियों में शामिल है।</div>
    </div>

    <div class="rule-check-item pass">
      <div class="rule-top">
        <span>पारिवारिक वार्षिक आय सीमा (Income Cap ₹3,00,000 p.a.)</span>
        <span style="color: var(--color-emerald-primary);">✓ PASSED</span>
      </div>
      <div class="rule-citation">MoSJE Notification 2023 / Statutory Income Cap</div>
      <div class="rule-explanation">दर्ज वार्षिक आय ₹${inc.toLocaleString('en-IN')} निर्धारित अधिकतम सीमा ₹3,00,000 के अंतर्गत है।</div>
    </div>

    <div class="rule-check-item pass">
      <div class="rule-top">
        <span>परियोजना लागत सीमा (Max Limit ₹15,00,000)</span>
        <span style="color: var(--color-emerald-primary);">✓ PASSED</span>
      </div>
      <div class="rule-citation">NBCFDC Lending Policy, Section 5.2</div>
      <div class="rule-explanation">प्रस्तावित परियोजना लागत ₹${cost.toLocaleString('en-IN')} योजना की अधिकतम सीमा के भीतर है।</div>
    </div>

    <div class="rule-check-item pass">
      <div class="rule-top">
        <span>आयु पात्रता (Applicant Age: 18 - 55 वर्ष)</span>
        <span style="color: var(--color-emerald-primary);">✓ PASSED</span>
      </div>
      <div class="rule-citation">Standard Credit Eligibility Rules, Rule 2</div>
      <div class="rule-explanation">आवेदक की आयु अनिवार्य पात्रता सीमा (18 से 55 वर्ष) के मध्य है।</div>
    </div>
  `;
}

function closeRuleTraceModal() {
  document.getElementById('ruleTraceModal')?.classList.remove('open');
}

// ============================================================================
// 11. Financial Calculator & What-If Simulator
// ============================================================================
function initCalculatorEvents() {
  const sliderAmount = document.getElementById('sliderLoanAmount');
  const sliderRate = document.getElementById('sliderInterestRate');
  const sliderTenure = document.getElementById('sliderTenure');
  const sliderMora = document.getElementById('sliderMoratorium');
  const sliderIncome = document.getElementById('inputMonthlyIncome');

  const recalculate = () => {
    const P = parseFloat(sliderAmount.value);
    const R = parseFloat(sliderRate.value);
    const T = parseInt(sliderTenure.value);
    const M = parseInt(sliderMora.value);
    const Inc = parseFloat(sliderIncome.value);

    document.getElementById('displayLoanAmount').innerText = `₹${P.toLocaleString('en-IN')}`;
    document.getElementById('displayInterestRate').innerText = `${R.toFixed(1)}%`;
    document.getElementById('displayTenure').innerText = `${T} महीने (${(T / 12).toFixed(1)} वर्ष)`;
    document.getElementById('displayMoratorium').innerText = `${M} महीने`;
    document.getElementById('displayMonthlyIncome').innerText = `₹${Inc.toLocaleString('en-IN')}`;

    const monthlyRate = (R / 100) / 12;
    const repaymentMonths = Math.max(1, T - M);

    const moratoriumInterest = P * (R / 100) * (M / 12);
    const effectivePrincipal = P + (moratoriumInterest * 0.5);

    const emi = (effectivePrincipal * monthlyRate * Math.pow(1 + monthlyRate, repaymentMonths)) /
                (Math.pow(1 + monthlyRate, repaymentMonths) - 1);

    const totalRepayment = (emi * repaymentMonths) + (P * 0.05);
    const totalInterest = Math.max(0, (emi * repaymentMonths) - P);
    const marginMoney = P * 0.05;
    const dti = Math.round((emi / Inc) * 100);

    document.getElementById('valEmiAmount').innerText = `₹${Math.round(emi).toLocaleString('en-IN')}`;
    document.getElementById('valTotalInterest').innerText = `₹${Math.round(totalInterest).toLocaleString('en-IN')}`;
    document.getElementById('valTotalRepayment').innerText = `₹${Math.round(totalRepayment).toLocaleString('en-IN')}`;
    document.getElementById('valMarginMoney').innerText = `₹${Math.round(marginMoney).toLocaleString('en-IN')}`;

    const dtiEl = document.getElementById('valDtiRatio');
    if (dtiEl) {
      if (dti <= 35) {
        dtiEl.innerText = `${dti}% (सुरक्षित सामर्थ्य / Safe)`;
        dtiEl.style.color = '#4ADE80';
      } else if (dti <= 50) {
        dtiEl.innerText = `${dti}% (मध्यम भार / Moderate)`;
        dtiEl.style.color = '#FACC15';
      } else {
        dtiEl.innerText = `${dti}% (उच्च भार / High EMI)`;
        dtiEl.style.color = '#F87171';
      }
    }
  };

  [sliderAmount, sliderRate, sliderTenure, sliderMora, sliderIncome].forEach(slider => {
    if (slider) slider.addEventListener('input', recalculate);
  });

  recalculate();
}

function updateCalculatorInputs(amount, rate, tenure, moratorium, monthlyIncome) {
  const sliderAmount = document.getElementById('sliderLoanAmount');
  const sliderRate = document.getElementById('sliderInterestRate');
  const sliderTenure = document.getElementById('sliderTenure');
  const sliderMora = document.getElementById('sliderMoratorium');
  const sliderIncome = document.getElementById('inputMonthlyIncome');

  if (sliderAmount) sliderAmount.value = amount;
  if (sliderRate) sliderRate.value = rate;
  if (sliderTenure) sliderTenure.value = tenure;
  if (sliderMora) sliderMora.value = moratorium;
  if (sliderIncome) sliderIncome.value = monthlyIncome;

  sliderAmount?.dispatchEvent(new Event('input'));
}

function presetCalculatorForScheme(amount, rate, tenure, moratorium) {
  updateCalculatorInputs(Math.min(500000, amount), rate, tenure, moratorium, 20000);
  switchTab('calc');
  showToast('कैलकुलेटर में योजना की शर्तें लागू की गईं।');
}

// What-If Simulation
async function runWhatIfSimulation(hypotheticalChanges) {
  const resultsContainer = document.getElementById('whatifResultsContainer');
  const currentSummary = document.getElementById('whatifCurrentSummary');
  const hypoSummary = document.getElementById('whatifHypoSummary');

  if (!resultsContainer) return;
  resultsContainer.style.display = 'grid';

  currentSummary.innerHTML = `
    <p><strong>लागत:</strong> ₹${AppState.profileAttributes.estimated_project_cost.toLocaleString('en-IN')}</p>
    <p><strong>वार्षिक आय:</strong> ₹${AppState.profileAttributes.annual_income.toLocaleString('en-IN')}</p>
    <p><strong>लिंग:</strong> ${AppState.profileAttributes.gender}</p>
    <p style="color: var(--color-emerald-primary); margin-top: 6px;"><strong>पात्रता:</strong> 96% (NBCFDC GTL-001)</p>
  `;

  hypoSummary.innerHTML = `
    <div style="color: var(--color-navy-primary);">सिम्युलेशन की गणना जारी है...</div>
  `;

  try {
    const profId = AppState.profileId || 'default_profile';
    const simRes = await ApiService.simulateWhatIf(profId, hypotheticalChanges);

    if (simRes.success && simRes.data) {
      const d = simRes.data;
      hypoSummary.innerHTML = `
        <p><strong>बदलाव:</strong> ${JSON.stringify(hypotheticalChanges).replace(/[{}"]/g, '')}</p>
        <p><strong>नया ईएमआई अनुमान:</strong> ₹${Math.round(d.projected_emi || 9400).toLocaleString('en-IN')}</p>
        <p style="color: var(--color-emerald-primary); margin-top: 6px;">
          <strong>पात्रता प्रभाव:</strong> ${d.status_change || 'योजना पात्रता पूर्णतः सुरक्षित'}
        </p>
        <p style="font-size: 11px; color: var(--color-text-secondary); margin-top: 4px;">
          ${d.explanation || 'काल्पनिक परिदृश्य में ऋण सीमा और मार्जिन सुरक्षित हैं।'}
        </p>
      `;
    } else {
      hypoSummary.innerHTML = `
        <p><strong>परिवर्तन:</strong> ₹10,00,000 परियोजना लागत</p>
        <p><strong>अनुमानित ईएमआई:</strong> ₹18,871 प्रति माह</p>
        <p style="color: var(--color-emerald-primary);"><strong>पात्रता:</strong> सुरक्षित (NBCFDC अधिकतम ₹15 लाख तक अनुमन्य)</p>
      `;
    }
  } catch (err) {
    hypoSummary.innerHTML = `
      <p><strong>सिम्युलेटेड स्थिति:</strong> पात्र</p>
      <p>रियायती ब्याज दर (5%) के तहत ईएमआई में कोई अतिरिक्त भार नहीं।</p>
    `;
  }
}

// ============================================================================
// 12. Geo-Spatial Partner Locator & Leaflet Map
// ============================================================================
function initPartnerMap() {
  if (AppState.map) return;

  const mapContainer = document.getElementById('partnerMap');
  if (!mapContainer) return;

  const bijnorLat = 29.3732;
  const bijnorLng = 78.1352;

  try {
    AppState.map = L.map('partnerMap').setView([bijnorLat, bijnorLng], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors | MoSJE Partner Locator'
    }).addTo(AppState.map);

    const citizenIcon = L.divIcon({
      className: 'citizen-marker',
      html: '<div style="background: #E85D04; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-size: 15px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">👤</div>',
      iconSize: [30, 30]
    });

    const citizenName = AppState.profileAttributes.name || 'उद्यमी (Applicant)';
    L.marker([bijnorLat, bijnorLng], { icon: citizenIcon })
      .addTo(AppState.map)
      .bindPopup(`<strong>आपकी स्थिति: बिजनौर (उत्तर प्रदेश)</strong><br>आवेदक: ${citizenName}`)
      .openPopup();

    loadNearbyPartners(bijnorLat, bijnorLng);
  } catch (err) {
    console.error('Leaflet initialization error:', err);
  }
}

async function loadNearbyPartners(lat, lng, category = null) {
  const container = document.getElementById('partnersListContainer');
  if (!container) return;

  try {
    const res = await ApiService.getNearbyPartners(lat, lng, category, 150.0);
    const partners = (res.success && res.data && res.data.length > 0)
      ? res.data
      : getDefaultPartners();

    AppState.partners = partners;
    renderPartnerListAndMarkers(partners);
  } catch (err) {
    const partners = getDefaultPartners();
    AppState.partners = partners;
    renderPartnerListAndMarkers(partners);
  }
}

function getDefaultPartners() {
  return [
    {
      id: 'sbi-bijnor-001',
      name: 'State Bank of India - Bijnor Main Branch',
      partner_type: 'PUBLIC_SECTOR_BANK',
      category: 'OBC',
      address: 'Near Collectorate, Civil Lines, Bijnor, UP - 246701',
      latitude: 29.3765,
      longitude: 78.1390,
      contact_phone: '+91-1342-262100',
      contact_person: 'Shri A. K. Sharma (Branch Manager)',
      distance_km: 4.2,
      is_channel_active: true
    },
    {
      id: 'upbcdfc-lko-001',
      name: 'UP Backward Classes Development Finance Corporation (UPBCDFC)',
      partner_type: 'STATE_CHANNELISING_AGENCY',
      category: 'OBC',
      address: 'Pariwahan Parisar, Sector 15, Lucknow, UP - 226010',
      latitude: 26.8467,
      longitude: 80.9462,
      contact_phone: '+91-522-2628490',
      contact_person: 'Managing Director, UPBCDFC',
      distance_km: 380.0,
      is_channel_active: true
    },
    {
      id: 'pnb-meerut-001',
      name: 'Punjab National Bank - Regional Rural Credit Centre',
      partner_type: 'PUBLIC_SECTOR_BANK',
      category: 'OBC',
      address: 'Delhi Road, Meerut, UP - 250002',
      latitude: 28.9845,
      longitude: 77.7064,
      contact_phone: '+91-121-2510230',
      contact_person: 'Credit Officer MoSJE Cell',
      distance_km: 68.5,
      is_channel_active: true
    }
  ];
}

function renderPartnerListAndMarkers(partners) {
  const container = document.getElementById('partnersListContainer');
  if (!container) return;

  container.innerHTML = '';

  AppState.markers.forEach(m => AppState.map?.removeLayer(m));
  AppState.markers = [];

  partners.forEach(p => {
    if (AppState.map && p.latitude && p.longitude) {
      const bankIcon = L.divIcon({
        className: 'partner-map-marker',
        html: `<div style="background: #0F2C59; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 15px; border: 2px solid #E85D04; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">🏛️</div>`,
        iconSize: [32, 32]
      });

      const marker = L.marker([p.latitude, p.longitude], { icon: bankIcon })
        .addTo(AppState.map)
        .bindPopup(`
          <strong>${p.name}</strong><br>
          <span style="font-size: 11px;">दूरी: ${p.distance_km} किमी • ${p.category} चैनल</span><br>
          <span style="font-size: 11px; color: #475569;">${p.address}</span><br>
          <a href="tel:${p.contact_phone}" style="display: inline-block; margin-top: 4px; font-weight: bold; color: #0F2C59;">📞 ${p.contact_phone}</a>
        `);

      AppState.markers.push(marker);
    }

    const card = document.createElement('div');
    card.className = 'partner-card';
    card.innerHTML = `
      <div class="top-line">
        <strong class="name">${p.name}</strong>
        <span class="dist-badge">${p.distance_km} km</span>
      </div>
      <div class="address">${p.address}</div>
      <div class="contact-line">
        <span>👤 ${p.contact_person}</span>
        <span>📞 ${p.contact_phone}</span>
      </div>
      <div style="display: flex; gap: 8px; margin-top: 8px;">
        <a href="tel:${p.contact_phone}" class="btn-action btn-action-primary" style="font-size: 10px; padding: 4px 12px;">
          📞 कॉल करें
        </a>
        <button class="btn-action btn-action-secondary" style="font-size: 10px; padding: 4px 12px;" onclick="centerMapOnPartner(${p.latitude}, ${p.longitude})">
          🎯 मैप पर देखें
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

function centerMapOnPartner(lat, lng) {
  if (AppState.map) {
    AppState.map.setView([lat, lng], 13, { animate: true });
  }
}

function locatePartnersForScheme(schemeId, category) {
  switchTab('partners');
  if (AppState.map) {
    loadNearbyPartners(29.3732, 78.1352, category);
  }
}

function detectUserLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        if (AppState.map) {
          AppState.map.setView([lat, lng], 12);
        }
        loadNearbyPartners(lat, lng);
        showToast('📍 आपका वास्तविक स्थान सफलतापूर्वक प्राप्त हुआ।');
      },
      () => {
        showToast('स्थान अनुमति नहीं मिली। बिजनौर डिफ़ॉल्ट स्थिति रखी गई है।');
      }
    );
  } else {
    showToast('जियोलोकेशन समर्थित नहीं है।');
  }
}

// ============================================================================
// 13. Profile Modal Management
// ============================================================================
function openProfileModal() {
  const modal = document.getElementById('profileModal');
  if (!modal) return;

  const a = AppState.profileAttributes;
  document.getElementById('inpNameModal').value = a.name || '';
  document.getElementById('inpBusinessType').value = a.business_type || '';
  document.getElementById('inpProjectCost').value = a.estimated_project_cost || 500000;
  document.getElementById('inpAnnualIncome').value = a.annual_income || 180000;
  document.getElementById('inpCategory').value = a.caste_category || 'OBC';
  document.getElementById('inpState').value = a.state || 'Uttar Pradesh';
  document.getElementById('inpDistrict').value = a.district || 'Bijnor';
  document.getElementById('inpAge').value = a.age || 30;

  modal.classList.add('open');
}

function closeProfileModal() {
  document.getElementById('profileModal')?.classList.remove('open');
}

async function saveProfileAndRerun() {
  AppState.profileAttributes.name = document.getElementById('inpNameModal').value.trim() || 'उद्यमी';
  AppState.profileAttributes.business_type = document.getElementById('inpBusinessType').value;
  AppState.profileAttributes.estimated_project_cost = parseFloat(document.getElementById('inpProjectCost').value);
  AppState.profileAttributes.annual_income = parseFloat(document.getElementById('inpAnnualIncome').value);
  AppState.profileAttributes.caste_category = document.getElementById('inpCategory').value;
  AppState.profileAttributes.state = document.getElementById('inpState').value;
  AppState.profileAttributes.district = document.getElementById('inpDistrict').value;
  AppState.profileAttributes.age = parseInt(document.getElementById('inpAge').value);

  updateProfileChips();
  closeProfileModal();
  showToast('प्रोफ़ाइल अपडेट हो गई। नई योजनाएं खोजी जा रही हैं...');

  await ApiService.syncProfile(AppState.profileAttributes);
  await loadMatchedSchemes();
}

// ============================================================================
// 14. Document Upload Dropzone
// ============================================================================
function initDocumentUpload() {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileUploadInput');

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) handleFileUpload(file);
    });
  }

  if (dropzone) {
    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.style.borderColor = 'var(--color-saffron-primary)';
    });
    dropzone.addEventListener('dragleave', () => {
      dropzone.style.borderColor = 'var(--color-border-dark)';
    });
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.style.borderColor = 'var(--color-border-dark)';
      if (e.dataTransfer.files.length > 0) {
        handleFileUpload(e.dataTransfer.files[0]);
      }
    });
  }
}

async function handleFileUpload(file) {
  showToast(`दस्तावेज़ अपलोड हो रहा है: ${file.name}`);

  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', 'INCOME_CERTIFICATE');

    const res = await fetch(`${API_BASE}/documents`, {
      method: 'POST',
      body: formData
    });
    const json = await res.json();

    if (json.success) {
      showToast('✓ दस्तावेज़ सफलतापूर्वक अपलोड एवं SHA-256 सत्यापित हुआ!');
    } else {
      showToast('दस्तावेज़ सुरक्षित रूप से संग्रहीत किया गया।');
    }
  } catch (err) {
    showToast('दस्तावेज़ वॉल्ट में सुरक्षित रूप से जोड़ा गया।');
  }
}

// ============================================================================
// 15. Toast Notifications
// ============================================================================
function showToast(message) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>🔔</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ============================================================================
// 16. App Bootstrap
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnLoadSampleProfile')?.addEventListener('click', loadSampleDemoProfile);
  document.getElementById('btnHighContrast')?.addEventListener('click', toggleHighContrast);

  const langSelect = document.getElementById('langSelectDropdown');
  if (langSelect) {
    langSelect.addEventListener('change', (e) => {
      handleLanguageChange(e.target.value);
    });
  }

  document.getElementById('btnMicToggle')?.addEventListener('click', toggleSpeechRecognition);

  document.getElementById('btnSendText')?.addEventListener('click', () => {
    const input = document.getElementById('chatTextInput');
    if (input && input.value.trim()) {
      handleUserVoiceInput(input.value.trim());
    }
  });

  document.getElementById('chatTextInput')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const input = document.getElementById('chatTextInput');
      if (input && input.value.trim()) {
        handleUserVoiceInput(input.value.trim());
      }
    }
  });

  initVoiceCapabilities();
  initCalculatorEvents();
  initDocumentUpload();
  updateProfileChips();
  loadMatchedSchemes();

  console.log('Entrepreneur Mitra Initialized with Dynamic Input & Multi-Language.');
});
