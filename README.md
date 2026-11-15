# DPG Engenharia Mecânica

Site institucional estático, responsivo e alinhado ao Manual da Marca DPG (outubro de 2026).

## Estrutura

- \`index.html\` — conteúdo, navegação, serviços e formulário de briefing.
- \`styles.css\` — layout responsivo e identidade visual.
- \`script.js\` — menu mobile, animações, ano automático e preparação de contato.
- \`logo.svg\` — assinatura DPG reproduzida a partir da arte incorporada ao manual enviado.
- \`favicon.svg\` — ícone do site.

## Identidade visual aplicada

- Grafite: \`#111820\`
- Azul técnico: \`#245BDB\`
- Preto: \`#000000\`
- Branco: \`#FFFFFF\`
- Apoio: \`#F2F4F7\` e \`#5B6470\`
- Tipografia: Arial
- Grafismos diagonais inspirados nos cortes do monograma.

## Configurar o WhatsApp

No início de \`script.js\`, preencha:

\`\`\`js
const WHATSAPP_NUMBER = "5532999999999";
\`\`\`

Use o número real com código do país e DDD, somente dígitos. O exemplo acima é ilustrativo. Enquanto o valor estiver vazio, o formulário prepara a mensagem e permite copiá-la. Não há envio de dados a um servidor externo.

## Publicação via GitHub Pages

1. Abra **Settings → Pages** no repositório.
2. Em **Build and deployment**, selecione **Deploy from a branch**.
3. Escolha a branch \`main\` e a pasta \`/(root)\`.
4. Salve e aguarde a publicação.

## Antes de divulgar

- Substitua a ilustração esquemática por registros reais de serviços quando houver imagens próprias e autorização para publicação.
- Revise os textos dos serviços e a adequação das atribuições profissionais ao escopo que será divulgado.
- Inclua WhatsApp, e-mail e número do CREA somente após confirmar os dados finais.
- A assinatura visual não substitui razão social, CNPJ, endereço ou outros dados cadastrais em documentos formais.

O formulário não utiliza backend. Imagens de projetos e clientes devem ser publicadas apenas com autorização, evitando dados internos, placas ou documentos sensíveis.