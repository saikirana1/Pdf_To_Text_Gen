import  { useEffect } from "react";
import IconButton from "@mui/material/IconButton";
import MicIcon from "@mui/icons-material/Mic";
import useSpeechToText from "react-hook-speech-to-text";

interface VoiceButtonProps {
  onTranscribe?: (text: string) => void; 
  onMicClick?: (isRecording: boolean) => void; 
}
function VoiceButton({ onTranscribe,onMicClick }:VoiceButtonProps) {
  const {
    isRecording,
    startSpeechToText,
    stopSpeechToText,
    interimResult,
  } = useSpeechToText({ continuous: true });
  useEffect(() => {
    if (onTranscribe && interimResult) {
      onTranscribe(interimResult);
    }
  }, [interimResult, onTranscribe]);

  const handleMicClick = () => {
    if (isRecording) {
      stopSpeechToText(); 
      console.log("🎤 Recording stopped");
    } else {
      startSpeechToText(); 
      console.log("🎙️ Recording started");
    }
     if (onMicClick) {
      onMicClick(isRecording);
    }
  };
 
  return (
    <IconButton
      color={isRecording ? "secondary" : "primary"} 
      onClick={handleMicClick} 
      size="large"
    >
      <MicIcon />
    </IconButton>
  );
}

export default VoiceButton;
