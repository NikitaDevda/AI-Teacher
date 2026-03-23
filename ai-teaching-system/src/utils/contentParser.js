// Structures content into organized sections
export const parseTeachingContent = (text) => {
  const sections = [];
  const lines = text.split('\n').filter(line => line.trim());
  
  let currentSection = null;
  
  lines.forEach((line) => {
    const trimmed = line.trim();
    
    // Skip very short or generic lines
    if (trimmed.length < 5) return;
    
    const lowerLine = trimmed.toLowerCase();
    
    // Skip common filler phrases
    const skipPhrases = ['namaste', 'hello', 'acha', 'toh', 'dekho', 'chaliye', 'basically', 'actually', 'let me', 'ab hum'];
    const shouldSkip = skipPhrases.some(phrase => 
      lowerLine.startsWith(phrase) && trimmed.length < 50
    );
    if (shouldSkip) return;
    
    // 1. DETECT HEADING (Title case, short, OR ends with colon)
    const isHeading = (
      (/^[A-Z][^.!?]*:$/.test(trimmed)) || // Ends with colon
      (trimmed.length < 60 && /^[A-Z]/.test(trimmed) && !trimmed.includes('.') && !trimmed.includes(',')) ||
      (/^#+\s/.test(trimmed)) // Markdown heading
    );
    
    if (isHeading) {
      // Save previous section
      if (currentSection) {
        sections.push(currentSection);
      }
      
      // Start new section
      currentSection = {
        heading: trimmed.replace(/^#+\s*/, '').replace(/:$/, ''),
        definition: null,
        points: []
      };
      return;
    }
    
    // If no section started yet, create one
    if (!currentSection) {
      currentSection = {
        heading: 'Key Concepts',
        definition: null,
        points: []
      };
    }
    
    // 2. DETECT DEFINITION (contains "is", "means", "called" near start)
    const isDefinition = (
      /^[A-Z][^:]*\s+(is|are|means|refers to|called|defined as)/i.test(trimmed) &&
      trimmed.length > 20 &&
      trimmed.length < 200
    );
    
    if (isDefinition && !currentSection.definition) {
      currentSection.definition = trimmed;
      return;
    }
    
    // 3. DETECT EQUATION/FORMULA
    const isEquation = (
      /[=+\-*/^²³√∫∑π]/.test(trimmed) || 
      /\b[a-z]\s*=\s*/.test(trimmed) ||
      /\d+\s*[+\-*/]\s*\d+/.test(trimmed)
    );
    
    if (isEquation) {
      currentSection.points.push({
        type: 'equation',
        text: trimmed
      });
      return;
    }
    
    // 4. DETECT BULLET POINTS (numbered, bullet, or keyword)
    const isBulletPoint = (
      /^(\d+[\.):]|•|\*|-|→|Step\s+\d+|Point\s+\d+)/i.test(trimmed) ||
      /^(feature|advantage|example|property|characteristic|step)/i.test(trimmed)
    );
    
    if (isBulletPoint) {
      currentSection.points.push({
        type: 'bullet',
        text: trimmed.replace(/^(\d+[\.):]|•|\*|-|→)\s*/, '')
      });
      return;
    }
    
    // 5. IMPORTANT KEY POINTS
    const isKeyPoint = /important|note|remember|yaad|dhyan|key/i.test(trimmed);
    
    if (isKeyPoint) {
      currentSection.points.push({
        type: 'keypoint',
        text: trimmed
      });
      return;
    }
    
    // 6. If line is substantial (>30 chars) and has content, add as point
    if (trimmed.length > 30 && /[a-zA-Z]/.test(trimmed)) {
      currentSection.points.push({
        type: 'text',
        text: trimmed
      });
    }
  });
  
  // Add last section
  if (currentSection && (currentSection.definition || currentSection.points.length > 0)) {
    sections.push(currentSection);
  }
  
  return sections;
};