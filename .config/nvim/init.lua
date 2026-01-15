-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")

vim.keymap.set('i','<C-Z>','<C-O>u',{silent = true })
vim.keymap.set("i", "<C-BS>", "<C-w>", { desc = "Delete word backwards" })
vim.keymap.set('i','<C-S-Z>','<C-O><C-R>',{silent = true })
vim.keymap.set('i',"<M-Up>", "<Esc>:m .-2<CR>==gi", { silent = true,desc = "Swap line with line above" })
vim.keymap.set('i',"<M-Down>", "<Esc>:m .+1<CR>==gi", { silent = true,desc = "Swap line with line below" })


-- Function to set keymaps with default options (noremap, silent)
local function map(mode, lhs, rhs, opts)
  local options = { noremap = true, silent = true }
  if opts then
    options = vim.tbl_extend('force', options, opts)
  end
  vim.api.nvim_set_keymap(mode, lhs, rhs, options)
end
map('i', '<C-S-Left>', '<C-O>vb<C-G>', { desc = "Select previous word in insert mode" })
map('i', '<C-S-Right>', '<C-O>vw<C-G>', { desc = "Select next word in insert mode" })



vim.keymap.set("v", "<A-Up>", ":m '<-2<CR>gv=gv", { silent = true })
vim.keymap.set("v", "<A-Down>", ":m '>+1<CR>gv=gv", { silent = true })