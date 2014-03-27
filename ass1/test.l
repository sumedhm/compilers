/*
Anjani Kumar 11101
Milind Solanki 11422
Sangharsh Aglave 11643
Sumedh Masulkar 11736
*/
digit [0-9]
letter [A-Fa-f]

%%

[+] {printf("(T_ADD, \"+\")\n");} 
[-] {printf("(T_SUB, \"-\")\n");}
[*] {printf("(T_MULT, \"*\")\n");}
[/] {printf("(T_DIV, \"/\")\n");}
(0x)({digit}|{letter})+ {printf("(T_HEX_INT, \" %s \")\n",yytext);}

({digit}+|{digit}*"."{digit}+)[E|e][+|-]?{digit}+ {printf("(T_EXP_REAL, \" %s \")\n",yytext);}

{digit}*"."{digit}+ {printf("(T_DOT_REAL, \" %s \")\n",yytext);}
{digit}+ {printf("(T_DEC_INT, \" %s \")\n",yytext);}
[(] {printf("(T_BRAC_BEGIN, \"(\")\n");}
[)] {printf("(T_BRAC_END, \")\")\n");}
. {printf("(INVALID_CHARACTER, \" %s \")\n", yytext);}
%%
	
int yywrap(void){
	return 1;
}

int main(void){
	yylex();
return 0;
}
