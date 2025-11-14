function getStjRoot(data) {
  if (data && typeof data === 'object') {
    if (data.stj && typeof data.stj === 'object') {
      return data.stj;
    }
    if (data.version && data.transcript) {
      return data;
    }
  }
  throw new Error('Invalid STJ file: missing "stj" root object');
}

function getTranscript(data) {
  const stjRoot = getStjRoot(data);
  if (!stjRoot.transcript || typeof stjRoot.transcript !== 'object') {
    throw new Error('Invalid STJ file: missing transcript section');
  }
  return stjRoot.transcript;
}

module.exports = {
  getStjRoot,
  getTranscript,
};
