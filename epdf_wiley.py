with open('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/new_wiley_links_2.txt', 'r') as old_file, open('new_wiley_links_3.txt', 'w') as new_file:
    for line in old_file:
        new_line = line.replace('/epdf/', '/pdfdirect/')
        if not new_line.endswith('?saml_referrer\n'):
            new_line = new_line.rstrip() + '?saml_referrer\n'
        new_file.write(new_line)

