const state = {
  token: localStorage.getItem('ttp_token'),
  user: null,
  ideas: [],
  sort: 'score'
};

const identityCard = document.getElementById('identity-card');
const ideaListEl = document.getElementById('idea-list');
const ideaStatus = document.getElementById('idea-status');
const sortSelect = document.getElementById('sort-select');

function headers() {
  const h = { 'Content-Type': 'application/json' };
  if (state.token) {
    h['Authorization'] = `Bearer ${state.token}`;
  }
  return h;
}

function setToken(token) {
  state.token = token;
  localStorage.setItem('ttp_token', token);
}

function clearToken() {
  state.token = null;
  state.user = null;
  localStorage.removeItem('ttp_token');
  renderIdentity();
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { ...headers(), ...(options.headers || {}) }
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || 'Request failed');
  }
  return response.json();
}

function renderIdentity() {
  if (!state.user) {
    identityCard.innerHTML = `
      <p class="label">Status</p>
      <h3>Not authenticated</h3>
      <p class="muted">Verify with Bank ID or government ID, then register to publish signed ideas.</p>
    `;
    return;
  }
  identityCard.innerHTML = `
    <p class="label">Verified identity</p>
    <h3>${state.user.display_name}</h3>
    <p class="muted">${state.user.legal_name || 'Verified person'} • ${state.user.identity_provider || 'identity provider'}</p>
    <p class="fingerprint">${state.user.fingerprint}</p>
    <p class="muted">Token stored locally. One verified person maps to one TTP account.</p>
    <button class="button button--ghost" id="logout-btn">Logout</button>
  `;
  document.getElementById('logout-btn').addEventListener('click', clearToken);
}

function attachTabHandlers() {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      tabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;
      document.querySelectorAll('[data-tab-content]').forEach((panel) => {
        panel.classList.toggle('hidden', panel.dataset.tabContent !== target);
      });
    });
  });
  document.getElementById('cta-register').addEventListener('click', () => tabs[0].click());
  document.getElementById('cta-login').addEventListener('click', () => tabs[1].click());
}

function parseTags(input) {
  return input
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);
}

function showError(target, message) {
  target.textContent = message;
  target.style.color = 'var(--danger)';
}

function showSuccess(target, message) {
  target.textContent = message;
  target.style.color = 'var(--accent)';
}

async function handleRegister(event) {
  event.preventDefault();
  const form = event.target;
  const payload = Object.fromEntries(new FormData(form));
  const authStatus = document.getElementById('auth-status');
  if (!payload.identity_verification_token) {
    try {
      const verification = await api('/api/identity/dev/verify', {
        method: 'POST',
        body: JSON.stringify({
          provider: payload.provider,
          subject_id: payload.subject_id,
          legal_name: payload.legal_name,
          country_code: 'SE'
        })
      });
      payload.identity_verification_token = verification.verification_token;
    } catch (err) {
      showError(authStatus, err.message);
      return;
    }
  }
  delete payload.provider;
  delete payload.subject_id;
  delete payload.legal_name;
  try {
    const data = await api('/api/register', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    setToken(data.token);
    state.user = data;
    renderIdentity();
    showSuccess(authStatus, 'Verified and signed in to TTP.');
  } catch (err) {
    showError(authStatus, err.message);
  }
}

async function handleLogin(event) {
  event.preventDefault();
  const form = event.target;
  const payload = Object.fromEntries(new FormData(form));
  try {
    const data = await api('/api/login', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    setToken(data.token);
    state.user = data;
    renderIdentity();
    showSuccess(document.getElementById('auth-status'), 'Signed in to TTP.');
  } catch (err) {
    showError(document.getElementById('auth-status'), err.message);
  }
}

async function hydrateUser() {
  if (!state.token) return;
  try {
    const me = await api('/api/me');
    state.user = me;
  } catch (err) {
    clearToken();
  }
}

function renderComments(container, idea) {
  const commentSection = document.createElement('div');
  commentSection.className = 'comment-section';
  const list = document.createElement('div');
  list.className = 'comment-list';
  commentSection.appendChild(list);

  const box = document.createElement('div');
  box.className = 'comment-box';
  box.innerHTML = `
    <textarea rows="2" placeholder="Add a discussion"></textarea>
    <button class="button button--ghost">Comment</button>
  `;
  box.querySelector('button').addEventListener('click', async () => {
    const body = box.querySelector('textarea').value.trim();
    if (!body) return;
    if (!state.token) return alert('Login to comment.');
    try {
      const comment = await api(`/api/ideas/${idea.id}/comments`, {
        method: 'POST',
        body: JSON.stringify({ body })
      });
      box.querySelector('textarea').value = '';
      prependComment(list, comment);
    } catch (err) {
      alert(err.message);
    }
  });
  commentSection.appendChild(box);
  container.appendChild(commentSection);

  // load existing
  api(`/api/ideas/${idea.id}/comments`)
    .then((comments) => {
      comments.forEach((c) => appendComment(list, c));
    })
    .catch(() => {});
}

function appendComment(list, comment) {
  const tpl = document.getElementById('comment-template');
  const node = tpl.content.cloneNode(true);
  node.querySelector('.comment__meta').textContent = `${comment.author.display_name} • ${new Date(comment.created_at).toLocaleString()}`;
  node.querySelector('.comment__body').textContent = comment.body;
  list.appendChild(node);
}

function prependComment(list, comment) {
  const tpl = document.getElementById('comment-template');
  const node = tpl.content.cloneNode(true);
  node.querySelector('.comment__meta').textContent = `${comment.author.display_name} • ${new Date(comment.created_at).toLocaleString()}`;
  node.querySelector('.comment__body').textContent = comment.body;
  list.prepend(node);
}

function renderIdeaCard(idea) {
  const card = document.createElement('article');
  card.className = 'idea-card';
  card.innerHTML = `
    <div class="idea-card__meta">${idea.author.display_name} • ${new Date(idea.created_at).toLocaleString()}</div>
    <h3 class="idea-card__title">${idea.title}</h3>
    <p>${idea.body}</p>
    <div class="idea-card__tags">${idea.tags.map((t) => `<span class="tag">${t}</span>`).join('')}</div>
    <div class="idea-card__meta">Status: ${idea.status}</div>
    <div class="signature">${idea.signature}</div>
    <div class="actions">
      <span class="score" data-score>${idea.score}</span>
      <button data-action="up">Upvote</button>
      <button data-action="down">Downvote</button>
      <button data-action="merge">Merge</button>
      <button data-action="edit">Edit</button>
      <button data-action="status">Status</button>
    </div>
    <div class="idea-card__meta">Fingerprint: ${idea.author.fingerprint}</div>
  `;

  const scoreEl = card.querySelector('[data-score]');
  card.querySelector('[data-action="up"]').addEventListener('click', () => handleVote(idea.id, 1, scoreEl));
  card.querySelector('[data-action="down"]').addEventListener('click', () => handleVote(idea.id, -1, scoreEl));
  card.querySelector('[data-action="merge"]').addEventListener('click', () => handleMerge(idea.id));
  card.querySelector('[data-action="edit"]').addEventListener('click', () => handleEdit(idea));
  card.querySelector('[data-action="status"]').addEventListener('click', () => handleStatus(idea));

  if (idea.merged_into_id) {
    const merged = document.createElement('div');
    merged.className = 'idea-card__meta';
    merged.textContent = `Merged into #${idea.merged_into_id}`;
    card.appendChild(merged);
  }

  renderComments(card, idea);
  return card;
}

async function handleStatus(idea) {
  if (!state.token) return alert('Login to update status.');
  const status = prompt('Set status: submitted, acknowledged, in_progress, resolved', idea.status);
  if (!status) return;
  try {
    await api(`/api/ideas/${idea.id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    });
    await loadIdeas();
  } catch (err) {
    alert(err.message);
  }
}

async function handleVote(id, value, scoreEl) {
  if (!state.token) return alert('Login to vote.');
  try {
    const { score } = await api(`/api/ideas/${id}/vote`, {
      method: 'POST',
      body: JSON.stringify({ value })
    });
    scoreEl.textContent = score;
  } catch (err) {
    alert(err.message);
  }
}

async function handleMerge(id) {
  if (!state.token) return alert('Login to merge.');
  const target = prompt('Merge into idea ID:');
  if (!target) return;
  try {
    await api(`/api/ideas/${id}/merge`, {
      method: 'POST',
      body: JSON.stringify({ target_id: Number(target) })
    });
    await loadIdeas();
  } catch (err) {
    alert(err.message);
  }
}

async function handleEdit(idea) {
  if (!state.token) return alert('Login to edit.');
  const title = prompt('Update title', idea.title);
  if (title === null) return;
  const body = prompt('Update body', idea.body);
  if (body === null) return;
  try {
    await api(`/api/ideas/${idea.id}`, {
      method: 'PUT',
      body: JSON.stringify({ title, body, tags: idea.tags })
    });
    await loadIdeas();
  } catch (err) {
    alert(err.message);
  }
}

async function loadIdeas() {
  try {
    const ideas = await api('/api/ideas');
    state.ideas = ideas;
    renderIdeas();
  } catch (err) {
    showError(ideaStatus, err.message);
  }
}

function renderIdeas() {
  ideaListEl.innerHTML = '';
  let ideas = [...state.ideas];
  if (state.sort === 'score') {
    ideas.sort((a, b) => b.score - a.score);
  } else {
    ideas.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }
  ideas.forEach((idea) => ideaListEl.appendChild(renderIdeaCard(idea)));
}

async function handleIdeaSubmit(event) {
  event.preventDefault();
  if (!state.token) {
    showError(ideaStatus, 'Please log in to publish.');
    return;
  }
  const form = event.target;
  const payload = Object.fromEntries(new FormData(form));
  payload.tags = parseTags(payload.tags || '');
  if (!payload.merged_into_id) delete payload.merged_into_id;
  try {
    await api('/api/ideas', { method: 'POST', body: JSON.stringify(payload) });
    form.reset();
    showSuccess(ideaStatus, 'Published with a fresh signature.');
    await loadIdeas();
  } catch (err) {
    showError(ideaStatus, err.message);
  }
}

async function loadSpec() {
  try {
    const spec = await api('/api/spec');
    document.getElementById('spec-body').textContent = spec.body;
  } catch (err) {
    document.getElementById('spec-body').textContent = 'Unable to load spec.';
  }
}

function attachFormHandlers() {
  document.getElementById('form-register').addEventListener('submit', handleRegister);
  document.getElementById('form-login').addEventListener('submit', handleLogin);
  document.getElementById('form-idea').addEventListener('submit', handleIdeaSubmit);
  sortSelect.addEventListener('change', (e) => {
    state.sort = e.target.value;
    renderIdeas();
  });
}

async function boot() {
  attachTabHandlers();
  attachFormHandlers();
  await hydrateUser();
  renderIdentity();
  await loadIdeas();
  await loadSpec();
}

boot();
