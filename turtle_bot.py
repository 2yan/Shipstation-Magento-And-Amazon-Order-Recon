from ryan_tools import * 
import amazon_parse
import magento_parse
import shipstation_parse
import glob
import os
import easygui
def write_header(writer):
    print('Writing Header')
    today = datetime.datetime.today()
    writer.writerow(['Made In Oregon', '','', '', '', '', 'as of', getdate(today) ])
    writer.writerow(['Stuck/ Unshipped Order Report'])
    writer.writerow([''])
    
    
def write_amazon(writer):
    print('Writing Amazon')
    today = datetime.datetime.today()
    writer.writerow(['Orders Outstanding/  FBMIO','', '', '', '','','', getdate(today - relativedelta(weeks = 1) ) + ' - ' + getdate(today)])
    writer.writerow(['Order #','Purchased On','Ship Date','Bill to Name','SKU','Status'])


    order_id_location = None
    purchase_date_location = None
    ship_date_location = None
    bill_to_name_location = None
    sku_location = None

    
    amazon_file  = None
    for file in glob.glob('*.txt'):
        amazon_file = open( file )

    i = 0
    for row in csv.reader(amazon_file, delimiter = '\t'):
        if i == 0:
            from ryan_tools import find_column_id as fc
            order_id_location = fc('order-id', row)
            purchase_date_location = fc('purchase-date', row)
            ship_date_location = fc('promise-date', row)
            bill_to_name_location = fc('buyer-name', row)
            sku_location = fc('sku', row)

        if i > 0:
            writer.writerow( [row[order_id_location], row[purchase_date_location][:10] ,  row[ship_date_location][:10], row[bill_to_name_location], row[sku_location], 'Unshipped'] )

            
        i = i + 1
                
def write_magento( writer, start_date, end_date ):
    print('Writing Magento & Adding Shipstation Data')
    writer.writerow(['Orders Outstanding/  Magento','','','','','','', getdate(start_date) + ' - ' + getdate(end_date) ])
    writer.writerow(['Order #',	'Purchased On',	'Ship Date', 'Ship to Name', 'G.T. (Purchased)', 'Magento Status', 'ShipStation Status', 'Reccomendation'])

    order_location = None
    purchased_date_location = None
    ship_date_location = None
    ship_to_name_location = None
    gt_location = None

    
    i = 0
    for row in csv.reader( open('orders.csv')):
        if i == 0:
            from ryan_tools import find_column_id as fc
            order_location = fc('Order #', row)
            purchased_date_location = fc('Purchased On', row)
            ship_date_location = fc('Ship Date', row)
            ship_to_name_location = fc('Ship to Name', row)
            gt_location = fc('G.T. (Base)', row)

        if i > 0:
            if 'A' not in row[order_location]:
                global user
                global password
                ship_station_status = shipstation_parse.download_status_by_order_number(str(row[order_location]), user, password)
                print(row[order_location],':',ship_station_status)
                ship_station_status = ship_station_status.lower()
                statuses = ['awaiting_shipment', 'shipped', 'cancelled', 'on_hold', 'not found']
                reccomendations = ['Ship', 'Update Magento', 'Create Credit Memo', 'Resolve Issue', 'Reconcile Shipstation']
                status_reccomendations_dict = dict(zip(statuses,reccomendations ))
                reccomendation = status_reccomendations_dict[ship_station_status]
                writer.writerow([ row[order_location], row[purchased_date_location], row[ship_date_location] , row[ship_to_name_location] , row[gt_location], 'Processing', ship_station_status, reccomendation  ])
        i = i + 1


def main(start_date,end_date):
    
    print('Downloading Amazon File')
    amazon_parse.download_orders_txt()
    print('Downloading Magento File')
    magento_parse.download_orders_csv(start_date, end_date)

    
    today = datetime.datetime.today()
    filename = today.strftime("%b") +' '+ str(today.day) +' ' +str(today.year) +  ' - Unshipped Order Report.csv'
    
    with open ( filename , 'w', newline = '') as csv_file:
        writer = csv.writer(csv_file,delimiter =',')
        write_header(writer)
        write_amazon(writer)
        
        writer.writerow('')
        write_magento(writer, start_date, end_date)
    input('Done! Enter to Open File')
    return filename

print('The Turtle Unshipped-Stuck Items Report Generator!')

user, password = easygui.multenterbox('SHIPSTATION API CREDENTIALS', fields= ['USERNAME', 'PASSWORD'] )

start_date, end_date = easygui.multenterbox('Start and End Dates?, Format = MM/DD/YYYY', fields= ['Start_date?', 'End_date?'] )
filename = main( read_date(start_date) , read_date(end_date))

os.system('"' + filename + '"')


