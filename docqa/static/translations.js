// Multilingual Translation System
const translations = {
  en: {
    // Common
    "title": "CP Office Smart Document Analysis",
    "uploadDoc": "Upload Document",
    "chatWithDocs": "Chat with Documents",
    "theme": "Theme",
    "language": "Language",
    
    // Upload Page
    "uploadNewDoc": "Upload New Document",
    "dropHere": "Drop PDF or Image here",
    "or": "or",
    "browseFiles": "Browse Files",
    "processBtn": "Process with Surya OCR",
    "processPlaceholder": "Drop your PDF or image here and begin smart processing with Surya OCR. The upload area is fully interactive and supports drag-and-drop.",
    "processedDocs": "Processed Documents",
    "yourRecentUploads": "Your recent uploads",
    "liveSync": "Live sync",
    "chat": "Chat →",
    "uploading": "Processing...",
    "uploadSuccess": "Upload Successful",
    "uploadSuccessMsg": "processed successfully!",
    "uploadFailed": "Upload Failed",
    "uploadProgress": "Uploading and extracting document...",
    "extractionComplete": "Extraction complete.",
    "extractionFailed": "Upload failed. Please retry.",
    
    // Chat Page
    "savedDocs": "Saved Documents",
    "chooseDocument": "Choose a document",
    "uploadedDoc": "Uploaded Document",
    "uploadedDocs": "Uploaded Documents",
    "askAboutDoc": "Ask anything about the selected document...",
    "askAnything": "Ask anything about the document...",
    "clearChat": "Clear Chat",
    "clearChatBtn": "Clear Chat",
    "chatCleared": "Chat cleared.",
    "stillConnected": "Still connected to",
    "connectedTo": "Connected to document:",
    "youCanAskQuestions": "You can now ask questions.",
    "docLoadedSuccessfully": "Document loaded successfully! You can now ask me anything about",
    "confirmDelete": "Confirm Deletion",
    "deleteConfirmMsg": "Are you sure you want to delete",
    "cancel": "Cancel",
    "delete": "Delete",
    "docDeleted": "Document Deleted",
    "docDeletedMsg": "has been deleted successfully.",
    "deletionFailed": "Deletion Failed",
    "deleteErrorMsg": "Error deleting document:",
    "networkError": "Network Error:",
    "error": "Error:",
    "ok": "OK",
  },
  hi: {
    // Common
    "title": "CP कार्यालय स्मार्ट दस्तावेज़ विश्लेषण",
    "uploadDoc": "दस्तावेज़ अपलोड करें",
    "chatWithDocs": "दस्तावेज़ों के साथ चैट करें",
    "theme": "थीम",
    "language": "भाषा",
    
    // Upload Page
    "uploadNewDoc": "नई दस्तावेज़ अपलोड करें",
    "dropHere": "यहाँ PDF या छवि छोड़ें",
    "or": "या",
    "browseFiles": "फ़ाइलें ब्राउज़ करें",
    "processBtn": "Surya OCR के साथ प्रक्रिया करें",
    "processPlaceholder": "अपनी PDF या छवि यहाँ छोड़ें और Surya OCR के साथ स्मार्ट प्रक्रिया शुरू करें। अपलोड क्षेत्र पूरी तरह से इंटरैक्टिव है और ड्रैग-एंड-ड्रॉप का समर्थन करता है।",
    "processedDocs": "प्रसंस्कृत दस्तावेज़",
    "yourRecentUploads": "आपके हाल के अपलोड",
    "liveSync": "लाइव सिंक",
    "chat": "चैट →",
    "uploading": "प्रक्रिया जारी है...",
    "uploadSuccess": "अपलोड सफल",
    "uploadSuccessMsg": "सफलतापूर्वक संसाधित!",
    "uploadFailed": "अपलोड विफल",
    "uploadProgress": "दस्तावेज़ अपलोड और निष्कर्षण...",
    "extractionComplete": "निष्कर्षण पूर्ण।",
    "extractionFailed": "अपलोड विफल। कृपया दोबारा प्रयास करें।",
    
    // Chat Page
    "savedDocs": "सहेजी गई दस्तावेज़ें",
    "chooseDocument": "एक दस्तावेज़ चुनें",
    "uploadedDoc": "अपलोड की गई दस्तावेज़",
    "uploadedDocs": "अपलोड की गई दस्तावेज़ें",
    "askAboutDoc": "चयनित दस्तावेज़ के बारे में कुछ भी पूछें...",
    "askAnything": "दस्तावेज़ के बारे में कुछ भी पूछें...",
    "clearChat": "चैट साफ़ करें",
    "clearChatBtn": "चैट साफ़ करें",
    "chatCleared": "चैट साफ़ किया गया।",
    "stillConnected": "अभी भी जुड़ा हुआ है",
    "connectedTo": "दस्तावेज़ से जुड़ा हुआ:",
    "youCanAskQuestions": "अब आप प्रश्न पूछ सकते हैं।",
    "docLoadedSuccessfully": "दस्तावेज़ सफलतापूर्वक लोड हो गया! आप अब मुझसे कुछ भी पूछ सकते हैं",
    "confirmDelete": "हटाने की पुष्टि करें",
    "deleteConfirmMsg": "क्या आप सुनिश्चित हैं कि आप हटाना चाहते हैं",
    "cancel": "रद्द करें",
    "delete": "हटाएं",
    "docDeleted": "दस्तावेज़ हटाया गया",
    "docDeletedMsg": "सफलतापूर्वक हटा दिया गया।",
    "deletionFailed": "हटाना विफल",
    "deleteErrorMsg": "दस्तावेज़ हटाने में त्रुटि:",
    "networkError": "नेटवर्क त्रुटि:",
    "error": "त्रुटि:",
    "ok": "ठीक है",
  },
  mr: {
    // Common
    "title": "CP कार्यालय स्मार्ट दस्तऐवज विश्लेषण",
    "uploadDoc": "दस्तऐवज अपलोड करा",
    "chatWithDocs": "दस्तऐवजांसह चॅट करा",
    "theme": "थीम",
    "language": "भाषा",
    
    // Upload Page
    "uploadNewDoc": "नवीन दस्तऐवज अपलोड करा",
    "dropHere": "येथे PDF किंवा प्रतिमा सोडा",
    "or": "किंवा",
    "browseFiles": "फाईल्स ब्राउজ करा",
    "processBtn": "Surya OCR सह प्रक्रिया करा",
    "processPlaceholder": "आपली PDF किंवा प्रतिमा येथे सोडा आणि Surya OCR सह स्मार्ट प्रक्रिया सुरू करा। अपलोड क्षेत्र पूर्णपणे परस्पर संवादी आहे आणि ड्रॅग-अँड-ड्रॉप समर्थन करते.",
    "processedDocs": "प्रक्रिया केलेले दस्तऐवज",
    "yourRecentUploads": "आपले अलीकडील अपलोड्स",
    "liveSync": "लाइव सिंक",
    "chat": "चॅट →",
    "uploading": "प्रक्रिया सुरू आहे...",
    "uploadSuccess": "अपलोड यशस्वी",
    "uploadSuccessMsg": "यशस्वीरित्या प्रक्रिया केली!",
    "uploadFailed": "अपलोड अयशस्वी",
    "uploadProgress": "दस्तऐवज अपलोड आणि काढणी...",
    "extractionComplete": "काढणी पूर्ण।",
    "extractionFailed": "अपलोड अयशस्वी. कृपया पुन्हा प्रयत्न करा.",
    
    // Chat Page
    "savedDocs": "जतन केलेले दस्तऐवज",
    "chooseDocument": "दस्तऐवज निवडा",
    "uploadedDoc": "अपलोड केलेले दस्तऐवज",
    "uploadedDocs": "अपलोड केलेले दस्तऐवज",
    "askAboutDoc": "निवडलेल्या दस्तऐवजाबद्दल काहीही विचारा...",
    "askAnything": "दस्तऐवजाबद्दल काहीही विचारा...",
    "clearChat": "चॅट साफ करा",
    "clearChatBtn": "चॅट साफ करा",
    "chatCleared": "चॅट साफ केला.",
    "stillConnected": "अजूनही जोडलेले",
    "connectedTo": "दस्तऐवजाशी जोडलेले:",
    "youCanAskQuestions": "आता आप प्रश्न विचारू शकता.",
    "docLoadedSuccessfully": "दस्तऐवज यशस्वीरित्या लोड झाला! आता आप मला काहीही विचारू शकता",
    "confirmDelete": "हटवण्याची पुष्टी करा",
    "deleteConfirmMsg": "आप निश्चित आहात की आप हटवू इच्छिता",
    "cancel": "रद्द करा",
    "delete": "हटवा",
    "docDeleted": "दस्तऐवज हटवला",
    "docDeletedMsg": "यशस्वीरित्या हटवला.",
    "deletionFailed": "हटवणे अयशस्वी",
    "deleteErrorMsg": "दस्तऐवज हटवण्यात त्रुटी:",
    "networkError": "नेटवर्क त्रुटी:",
    "error": "त्रुटी:",
    "ok": "ठीक आहे",
  }
};

// Language Management
class LanguageManager {
  constructor() {
    this.currentLanguage = localStorage.getItem('suryaLanguage') || 'en';
  }

  setLanguage(lang) {
    if (lang in translations) {
      this.currentLanguage = lang;
      localStorage.setItem('suryaLanguage', lang);
      this.updatePageLanguage();
    }
  }

  getLanguage() {
    return this.currentLanguage;
  }

  t(key) {
    return translations[this.currentLanguage][key] || translations['en'][key] || key;
  }

  updatePageLanguage() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const key = element.getAttribute('data-i18n');
      element.textContent = this.t(key);
    });

    // Update all placeholders with data-i18n-placeholder attribute
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
      const key = element.getAttribute('data-i18n-placeholder');
      element.placeholder = this.t(key);
    });

    // Update page title
    document.title = this.t('title');

    // Trigger custom event for app-specific updates
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: this.currentLanguage } }));
  }
}

// Initialize Language Manager
const langManager = new LanguageManager();

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  langManager.updatePageLanguage();
  
  // Setup language selector if it exists
  const langSelector = document.getElementById('language-selector');
  if (langSelector) {
    langSelector.value = langManager.getLanguage();
    langSelector.addEventListener('change', (e) => {
      langManager.setLanguage(e.target.value);
    });
  }
});
